// FILE: KOTLIN/AqarionAgent.kt — A15 on-device verifier
package org.aqarion

import java.io.File

object AqarionAgent {
    data class Receipt(
        val contract: String,
        val cases: Int,
        val maxTraceErr: Double,
        val maxNormErr: Double,
        val status: String
    )

    fun replay(contract: String = "SV-001-V2"): Receipt {
        // 1. Load aqarion.toml
        val toml = File("aqarion.toml").readText()

        // 2. Resolve artifact path for contract
        val artifactPath = when(contract) {
            "S13" -> "VERIFICATION/AQ-S13-CHECK.PY"
            else -> "VERIFICATION/AQ-S13-CHECK.PY"
        }

        // 3. Run Python — Chaquopy on Android, python3 on desktop/Termux
        val output = runPython(artifactPath)

        // 4. Parse output for receipt
        val cases = Regex("total=(\\d+)").find(output)?.groupValues?.get(1)?.toInt()?: 0
        val traceErr = Regex("Trace max err ([\\deE+\\-\\.]+)").find(output)?.groupValues?.get(1)?.toDouble()?: 99.0
        val normErr = Regex("Op-norm max err ([\\deE+\\-\\.]+)").find(output)?.groupValues?.get(1)?.toDouble()?: 99.0

        val status = if (cases==5720 && traceErr<1e-12 && normErr<1e-12) "REPLAYED" else "FAILED"

        val receipt = Receipt(contract, cases, traceErr, normErr, status)
        File("receipts/${contract}.json").apply {
            parentFile.mkdirs()
            writeText("""
            {
              "contract": "${receipt.contract}",
              "cases": ${receipt.cases},
              "max_trace_err": ${receipt.maxTraceErr},
              "max_norm_err": ${receipt.maxNormErr},
              "status": "${receipt.status}",
              "governance": "C4=BLOCKED"
            }
            """.trimIndent())
        }
        return receipt
    }

    private fun runPython(path: String): String {
        return try {
            // Termux / Chaquopy fallback
            val proc = Runtime.getRuntime().exec(arrayOf("python3", path))
            proc.inputStream.bufferedReader().readText() + proc.errorStream.bufferedReader().readText()
        } catch (e: Exception) {
            "ENVIRONMENT_BLOCKED: ${e.message}"
        }
    }
}

// Usage on A15:
// AqarionAgent.replay("S13") -> writes receipts/S13.json
