import io.gatling.core.Predef._

import scala.concurrent.duration._

/**
  * Created by mho on 02/05/17.
  */

class StaresRamp extends DruidSineSignalSimulation {

  val simulationParameters: Map[String, Int] = Map(
    "m" -> {{ simulation.duration.minutes }},
    "s" -> {{ simulation.duration.seconds }},
    "nbSensors" -> {{ simulation.nbSensors }}
  )

  println(simulationParameters.toString())
  Thread.sleep(5000)

  val sensor = scenario("Several sensors send 1 measure: I following a stares-shaped signal")
    .feed(this.Write.rteIntensityFeeder)
    .exec(this.Write.write("I"))

  setUp(
    this.sensor.inject(
      constantUsersPerSec(simulationParameters("nbSensors")) during(1 minute)
    ).protocols(httpConf))
}
