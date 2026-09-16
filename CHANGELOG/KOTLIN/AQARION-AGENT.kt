package org.aqarion
import java.io.File
import java.security.MessageDigest
object AqarionAgent {
    data class Receipt(val contract:String,val cases:Int,val maxTraceErr:Double,val maxNormErr:Double,val status:String,val artifactSha256:String)
    fun loadToml():String=File("aqarion.toml").readText()
    fun resolveArtifact(c:String,t:String):Pair<String,String> = when(c){
        "SV-001-V2"->Pair("VERIFICATION/sv001_v2_check.py","auto")
        "S13"->Pair("VERIFICATION/AQ-S13-CHECK.PY","auto")
        else->Pair("VERIFICATION/sv001_v2_check.py","auto")
    }
    fun sha256OfFile(p:String):String{
        val md=MessageDigest.getInstance("SHA-256")
        return md.digest(File(p).readBytes()).joinToString(""){"%02x".format(it)}
    }
    fun replay(contract:String="SV-001-V2"):Receipt{
        val (artifactPath,_)=resolveArtifact(contract,loadToml())
        val sha=try{sha256OfFile(artifactPath)}catch(e:Exception){"MISSING"}
        val out=runPython(artifactPath)
        val cases=Regex("total=(\\d+)").find(out)?.groupValues?.get(1)?.toInt()?:0
        val traceErr=Regex("Trace max err ([\\deE+\\-\\.]+)").find(out)?.groupValues?.get(1)?.toDouble()?:99.0
        val normErr=Regex("Op-norm max err ([\\deE+\\-\\.]+)").find(out)?.groupValues?.get(1)?.toDouble()?:99.0
        val status=if(cases==5720&&traceErr<1e-12&&normErr<1e-12)"REPLAYED" else "FAILED"
        val r=Receipt(contract,cases,traceErr,normErr,status,sha)
        File("receipts/${contract}.json").apply{
            parentFile.mkdirs()
            writeText("""{"contract":"${r.contract}","cases":${r.cases},"max_trace_err":${r.maxTraceErr},"max_norm_err":${r.maxNormErr},"status":"${r.status}","artifact_sha256":"${r.artifactSha256}","governance":"C4=BLOCKED"}""")
        }
        return r
    }
    private fun runPython(p:String):String{
        return try{Runtime.getRuntime().exec(arrayOf("python3",p)).inputStream.bufferedReader().readText()}catch(e:Exception){"ENVIRONMENT_BLOCKED: ${e.message}"}
    }
}
