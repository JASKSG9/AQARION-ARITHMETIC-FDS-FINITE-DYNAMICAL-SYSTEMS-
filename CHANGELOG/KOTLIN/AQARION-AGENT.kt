package org.aqarion

import java.io.File
import java.util.UUID
import java.util.concurrent.TimeUnit

object AqarionAgent {

    private const val CONTRACT = "SV-001-V2"

    private const val EXPECTED_CASES = 1176

    data class Receipt(
        val contract: String,
        val cases: Int,
        val maxGramErr: Double,
        val maxNormErr: Double,
        val status: String,
        val governance: String,
        val processExitCode: Int?
    )

    fun replay(): Receipt {

        val receiptId = UUID
            .randomUUID()
            .toString()

        val rawPath =
            "receipts/raw_sv001_$receiptId.json"

        val metaPath =
            "receipts/meta_sv001_$receiptId.json"

        val rawFile = File(rawPath)
        val metaFile = File(metaPath)

        val verifierResult =
            runProcess(
                listOf(
                    "python3",
                    "VERIFICATION/sv001_v2_check.py",
                    "--json-output",
                    rawPath
                )
            )

        if (
            verifierResult.exitCode != 0
            || !rawFile.exists()
        ) {
            return persist(
                Receipt(
                    contract = CONTRACT,
                    cases = 0,
                    maxGramErr = Double.NaN,
                    maxNormErr = Double.NaN,
                    status = "FAILED",
                    governance = "C4=BLOCKED",
                    processExitCode =
                        verifierResult.exitCode
                )
            )
        }

        val metaResult =
            runProcess(
                listOf(
                    "python3",
                    "VERIFICATION/sv001_receipt_check.py",
                    rawPath
                )
            )

        if (
            metaResult.exitCode != 0
        ) {
            return persist(
                Receipt(
                    contract = CONTRACT,
                    cases = 0,
                    maxGramErr = Double.NaN,
                    maxNormErr = Double.NaN,
                    status = "FAILED_META",
                    governance = "C4=BLOCKED",
                    processExitCode =
                        metaResult.exitCode
                )
            )
        }

        /*
         * IMPORTANT:
         *
         * Replace this minimal extraction with the JSON parser
         * already pinned by the AQARION build.
         *
         * Do not use regex as a certificate parser.
         */

        val jsonText =
            rawFile.readText()

        val cases =
            jsonInt(
                jsonText,
                "cases_executed"
            )

        val maxGramErr =
            jsonDouble(
                jsonText,
                "max_gram_error"
            )

        val maxNormErr =
            jsonDouble(
                jsonText,
                "max_norm_error"
            )

        val status =
            jsonString(
                jsonText,
                "status"
            )

        val replayStatus =
            if (
                status == "PASS"
                && cases == EXPECTED_CASES
                && maxGramErr.isFinite()
                && maxNormErr.isFinite()
                && maxGramErr <= 1e-12
                && maxNormErr <= 1e-12
            ) {
                "REPLAYED"
            } else {
                "FAILED_POLICY"
            }

        rawFile.delete()
        metaFile.delete()

        return persist(
            Receipt(
                contract = CONTRACT,
                cases = cases,
                maxGramErr = maxGramErr,
                maxNormErr = maxNormErr,
                status = replayStatus,
                governance = "C4=BLOCKED",
                processExitCode =
                    verifierResult.exitCode
            )
        )
    }

    private data class ProcessResult(
        val output: String,
        val exitCode: Int?
    )

    private fun runProcess(
        command: List<String>
    ): ProcessResult {

        return try {

            val process =
                ProcessBuilder(command)
                    .redirectErrorStream(true)
                    .start()

            val output =
                process
                    .inputStream
                    .bufferedReader()
                    .readText()

            val completed =
                process.waitFor(
                    30,
                    TimeUnit.SECONDS
                )

            if (!completed) {
                process.destroyForcibly()

                return ProcessResult(
                    "TIMEOUT_EXCEEDED",
                    null
                )
            }

            ProcessResult(
                output,
                process.exitValue()
            )

        } catch (e: Exception) {

            ProcessResult(
                "EXECUTION_ERROR: ${e.message}",
                null
            )
        }
    }

    private fun persist(
        receipt: Receipt
    ): Receipt {

        val file =
            File(
                "receipts/$CONTRACT.json"
            )

        file.parentFile?.mkdirs()

        file.writeText(
            """
            {
              "contract": "${receipt.contract}",
              "cases": ${receipt.cases},
              "max_gram_err": ${receipt.maxGramErr},
              "max_norm_err": ${receipt.maxNormErr},
              "status": "${receipt.status}",
              "governance": "${receipt.governance}",
              "process_exit_code": ${receipt.processExitCode}
            }
            """.trimIndent()
        )

        return receipt
    }

    /*
     * Transitional helpers only.
     *
     * Production policy:
     * migrate to the repository's pinned JSON parser
     * before promotion above C4 BLOCKED.
     */

    private fun jsonInt(
        json: String,
        key: String
    ): Int {

        return Regex(
            "\"$key\"\\s*:\\s*(\\d+)"
        )
            .find(json)
            ?.groupValues
            ?.get(1)
            ?.toInt()
            ?: -1
    }

    private fun jsonDouble(
        json: String,
        key: String
    ): Double {

        return Regex(
            "\"$key\"\\s*:\\s*([\\deE+\\-\\.]+)"
        )
            .find(json)
            ?.groupValues
            ?.get(1)
            ?.toDoubleOrNull()
            ?: Double.NaN
    }

    private fun jsonString(
        json: String,
        key: String
    ): String {

        return Regex(
            "\"$key\"\\s*:\\s*\"([^\"]+)\""
        )
            .find(json)
            ?.groupValues
            ?.get(1)
            ?: ""
    }
}
