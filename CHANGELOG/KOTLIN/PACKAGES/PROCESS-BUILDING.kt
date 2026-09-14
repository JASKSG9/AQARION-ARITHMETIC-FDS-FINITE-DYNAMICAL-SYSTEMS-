package org.aqarion

import java.io.File
import java.nio.charset.StandardCharsets
import java.security.MessageDigest
import java.util.concurrent.TimeUnit

object AqarionAgent {
    enum class ReplayStatus {
        REPLAYED,
        FAILED,
        TIMEOUT,
        ENVIRONMENT_BLOCKED,
        CONTRACT_INVALID,
        ARTIFACT_HASH_MISMATCH,
        RECEIPT_INVALID
    }

    data class ReplayResult(
        val contract: String,
        val status: ReplayStatus,
        val exitCode: Int?,
        val timedOut: Boolean,
        val stdoutPath: String,
        val verifierJsonPath: String?,
        val artifactSha256: String?,
        val message: String
    )

    fun sha256(file: File): String {
        val digest = MessageDigest.getInstance("SHA-256")

        file.inputStream().use { input ->
            val buffer = ByteArray(1024 * 1024)

            while (true) {
                val read = input.read(buffer)

                if (read < 0) {
                    break
                }

                digest.update(buffer, 0, read)
            }
        }

        return digest.digest().joinToString("") { "%02x".format(it) }
    }

    fun replay(
        projectRoot: File,
        contract: String = "SV-001-V2",
        timeoutSeconds: Long = 45
    ): ReplayResult {
        val verifier = File(projectRoot, "VERIFICATION/sv001_v2_check.py")
        val receiptDir = File(projectRoot, "RECEIPTS")
        val stdoutFile = File(receiptDir, "$contract.stdout.txt")
        val verifierJson = File(receiptDir, "$contract.verifier.json")

        if (!verifier.isFile) {
            return ReplayResult(
                contract = contract,
                status = ReplayStatus.ENVIRONMENT_BLOCKED,
                exitCode = null,
                timedOut = false,
                stdoutPath = stdoutFile.path,
                verifierJsonPath = null,
                artifactSha256 = null,
                message = "Verifier script does not exist: ${verifier.path}"
            )
        }

        receiptDir.mkdirs()

        val scriptHash = sha256(verifier)

        val process = try {
            ProcessBuilder(
                "python3",
                verifier.path,
                "--json-output",
                verifierJson.path
            )
                .directory(projectRoot)
                .redirectErrorStream(true)
                .redirectOutput(stdoutFile)
                .start()
        } catch (error: Exception) {
            return ReplayResult(
                contract = contract,
                status = ReplayStatus.ENVIRONMENT_BLOCKED,
                exitCode = null,
                timedOut = false,
                stdoutPath = stdoutFile.path,
                verifierJsonPath = null,
                artifactSha256 = scriptHash,
                message = "Unable to start verifier: ${error.message}"
            )
        }

        val finished = process.waitFor(timeoutSeconds, TimeUnit.SECONDS)

        if (!finished) {
            process.destroy()

            if (!process.waitFor(2, TimeUnit.SECONDS)) {
                process.destroyForcibly()
            }

            return ReplayResult(
                contract = contract,
                status = ReplayStatus.TIMEOUT,
                exitCode = null,
                timedOut = true,
                stdoutPath = stdoutFile.path,
                verifierJsonPath = verifierJson.path.takeIf { it.isFile }?.path,
                artifactSha256 = scriptHash,
                message = "Verifier exceeded timeout of $timeoutSeconds seconds"
            )
        }

        val exitCode = process.exitValue()

        if (exitCode != 0) {
            return ReplayResult(
                contract = contract,
                status = ReplayStatus.FAILED,
                exitCode = exitCode,
                timedOut = false,
                stdoutPath = stdoutFile.path,
                verifierJsonPath = verifierJson.path.takeIf { it.isFile }?.path,
                artifactSha256 = scriptHash,
                message = "Verifier exited nonzero"
            )
        }

        if (!verifierJson.isFile) {
            return ReplayResult(
                contract = contract,
                status = ReplayStatus.RECEIPT_INVALID,
                exitCode = exitCode,
                timedOut = false,
                stdoutPath = stdoutFile.path,
                verifierJsonPath = null,
                artifactSha256 = scriptHash,
                message = "Verifier returned zero but produced no JSON result"
            )
        }

        return ReplayResult(
            contract = contract,
            status = ReplayStatus.REPLAYED,
            exitCode = exitCode,
            timedOut = false,
            stdoutPath = stdoutFile.path,
            verifierJsonPath = verifierJson.path,
            artifactSha256 = scriptHash,
            message = "Verifier completed; JSON requires separate schema validation"
        )
    }
}
