import java.time.{ZoneId, ZonedDateTime}

import io.gatling.core.feeder._

/**
  * Created by mho on 10/05/17.
  */

/**
  * A measure sent by a sensor is composed of
  * an id, a type of measure, an origine, a source, a validity and an ISO8601 timestamp
  */
trait Measure {
  def id(): Int
  val _type: Char = 'Z'
  def value: Double
  def origine: Int
  def source: Int
  def validite: Int
  def timestampToString: String = this.computeTimestampToString(this.computeTimestamp())

  private def computeTimestamp(): ZonedDateTime = {
    val region = "Europe/Paris"
    ZonedDateTime.now(ZoneId.of(region))
  }

  private def computeTimestampToString(ts: ZonedDateTime): String = {
    val dateNowAsString = ts.toString
    // Getting rid of the timezone in the string "timestamp[region]\EOC" --> "timestamp\EOC"
    dateNowAsString.dropRight(dateNowAsString.length - dateNowAsString.indexOf("["))
  }

  def toFeeder: Feeder[_]
}

/**
  * An RTE measure is a measure in which the components are specifically generated
  */
abstract class RteMeasure(val amplitude: Int, val shift: Int) extends Measure {

  // Needed generators to compose an RTEmeasure
  object sourceGenerator extends NumericGenerator(1, 5)
  object origineGenerator extends NumericGenerator(1, 10)
  object validiteGenerator extends NumericGenerator(0, 1)
  object sineValueGenerator extends SineValueGenerator(amplitude, shift)
  object typeGenerator extends DataGeneratorTrait {
    val pool: Seq[Char] = Seq('I', 'P', 'Q')

    def generate(desiredType: Char): Char =
      if (this.pool.contains(desiredType)) desiredType
      else throw new IllegalArgumentException("Type de mesure non reconnue à la génération.")

    def apply(desiredState: Char): Char = this.generate(desiredState)
  }

  override def origine: Int = origineGenerator.generate()
  override def source: Int = sourceGenerator.generate()
  override def validite: Int = validiteGenerator.generate()
  override def value: Double = sineValueGenerator.generate()

  override def toFeeder: Feeder[_] = {
    Iterator.continually(Map[String, Any](
      "id".concat(this._type.toString) -> this.id,
      "type".concat(this._type.toString) -> this._type,
      "value".concat(this._type.toString) -> this.value,
      "validite".concat(this._type.toString) -> this.validite,
      "source".concat(this._type.toString) -> this.source,
      "origine".concat(this._type.toString) -> this.origine,
      "timestamp".concat(this._type.toString) -> this.timestampToString
    ))
  }

}

/**
  * Measure singleton -_- Measure Factory
  */
object Measure {

  /**
    * An RteIntensityMeasure is an RTEmeasure
    * that shares an id with other P & Q measures
    * and has a 'I' type
    */
  private class RteIntensityMeasure(val _idGen: NumericGenerator) extends RteMeasure(25, 0) {
    override def id(): Int = this._idGen.generate()
    override val _type: Char = 'I'

  }

  /**
    * An RtePowerMeasure is an RTEmeasure
    * that shares an id with other I & Q measures
    * and has a 'P' type
    */
  private class RtePowerMeasure(val _idGen: NumericGenerator) extends RteMeasure(45, 120) {
    override def id(): Int = this._idGen.generate()
    override val _type: Char = 'P'
//    object svgp extends PowerValueGenerator
//    override def value: Double = svgp.generate()
  }

  private class RteQuantityMeasure(val _idGen: NumericGenerator) extends RteMeasure(-3, 0) {
    override def id(): Int = this._idGen.generate()
    override val _type: Char = 'Q'
//    object svgq extends QuantityValueGenerator
//    override def value: Double = svgq.generate()
  }

  def apply(s: String, submittedIdGen: NumericGenerator): Measure = {
    s.toLowerCase match {
      case "intensity" => new RteIntensityMeasure(submittedIdGen)
      case "power" => new RtePowerMeasure(submittedIdGen)
      case "quantity" => new RteQuantityMeasure(submittedIdGen)
      case "i" => new RteIntensityMeasure(submittedIdGen)
      case "p" => new RtePowerMeasure(submittedIdGen)
      case "q" => new RteQuantityMeasure(submittedIdGen)
      case _ => throw new IllegalArgumentException("String identifier unexpected")
    }
  }
}




