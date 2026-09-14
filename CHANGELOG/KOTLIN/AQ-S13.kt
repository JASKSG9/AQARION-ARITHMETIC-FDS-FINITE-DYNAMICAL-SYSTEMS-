package org.aqarion
import java.io.File
import java.util.concurrent.TimeUnit
import kotlin.math.sqrt
object AqarionAgent {
 data class Receipt(val contract:String,val cases:Int,val maxTraceErr:Double,val maxNormErr:Double,val status:String,val tolerance:Double)
 fun replay(contract:String="SV-001-V2"): Receipt {
  val output=runPythonSafely("VERIFICATION/replay_harness.py")
  val cases=Regex("cases=(\\d+)").find(output)?.groupValues?.get(1)?.toInt()?:0
  val tErr=Regex("max_t=([\\deE+\\-\\.]+)").find(output)?.groupValues?.get(1)?.toDouble()?:Double.MAX_VALUE
  val nErr=Regex("max_n=([\\deE+\\-\\.]+)").find(output)?.groupValues?.get(1)?.toDouble()?:Double.MAX_VALUE
  val tol=1e-12*sqrt(cases.toDouble().coerceAtLeast(1.0))
  val status=if(cases==5720 && tErr<=tol && nErr<=tol) "REPLAYED" else "FAILED"
  val receipt=Receipt(contract,cases,tErr,nErr,status,tol)
  File("receipts/${contract}.json").apply{parentFile.mkdirs(); writeText("""{"contract":"${contract}","cases":${cases},"max_trace_err":${tErr},"max_norm_err":${nErr},"status":"${status}","governance":"C4=BLOCKED","tolerance_applied":${tol}}""")}
  return receipt
 }
 private fun runPythonSafely(path:String): String {
  return try {
   val pb=ProcessBuilder("python3",path); pb.redirectErrorStream(true)
   val proc=pb.start(); val out=proc.inputStream.bufferedReader().readText()
   proc.waitFor(45,TimeUnit.SECONDS); out
  } catch(e:Exception){ "ENVIRONMENT_BLOCKED ${e.message}" }
 }
}
