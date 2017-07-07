
import io.gatling.core.Predef._
import io.gatling.http.Predef._

/**
  * Created by mho on 04/05/17.
  */
abstract class DruidSineSignalSimulation extends Simulation {

  val tranquility: AbstractTranquility = new TranquilityInstance

  val httpConf = http.baseURL(tranquility.url)

  object idGeneratorI extends NumericGenerator(1, 100000)
  object idGeneratorP extends NumericGenerator(1, 100000)
  object idGeneratorQ extends NumericGenerator(1, 100000)

  object Write {

    val rteIntensityFeeder = Measure("I", idGeneratorI).toFeeder
    val rtePowerFeeder: Feeder[_] = Measure("P", idGeneratorP).toFeeder
    val rteQuantityFeeder: Feeder[_] = Measure("Q", idGeneratorQ).toFeeder

    def rteJSONbodyGenerator(_type: String): String = {
      """{
        |"id": "${id%s}",
        |"type": "${type%s}",
        |"value": "${value%s}",
        |"validite": "${validite%s}",
        |"source": "${source%s}",
        |"origine": "${origine%s}",
        |"timestamp": "${timestamp%s}"
        |}
        |""".format(_type, _type, _type, _type, _type, _type, _type)
    }


    def write(typeMeasure: String) = {
      exec(http("Sending point(s) to the Tranquility streaming server")
        .post(tranquility.requestPath)
        .body(StringBody(
          rteJSONbodyGenerator(typeMeasure)
          .stripMargin)
        ).asJSON
      )
    }


  }
}
