import scala.util.Random

/**
  * Created by mho on 12/05/17.
  */
trait DataGeneratorTrait {
  val pool: Seq[_]
}

abstract class NumericGenerator(val minVal: Int, val maxVal: Int) extends DataGeneratorTrait {

  if (this.minVal > this.maxVal) throw new IllegalStateException("minVal should be lesser than maxVal")

  val pool: Range = minVal to maxVal
  val numericIterator: Iterator[Int] = Iterator.continually(pool.toList).flatten//this.pool.iterator
  def generate(): Int = this.numericIterator.next
}

abstract class SineValueGenerator(val amplitude: Int, val shift: Int) extends DataGeneratorTrait {

  val period = 86400  // Period of the signal
  val frequency: Double = (period/4).toDouble
  val experienceSpanOfTime: Int = 3*period

  override val pool: Range = 0 to this.experienceSpanOfTime

  def mySine(A: Double, f: Double = this.frequency, P: Double, t: Double, shift: Int = 0, phase: Int = 0, randomDataPoint: Boolean = true, randomVerticalShift: Boolean = true, withPhase: Boolean = true): Double = {

    val rdp = if (randomDataPoint) Random.nextInt(2) else 0
    val rds = if(randomVerticalShift) Random.nextInt(15) else 0
    val ph = if(withPhase) phase else 0
    Math.abs(A) * Math.sin(t/f + ph) + (A + shift + rdp) + rds

  }

  val sineValues: List[Double] = {
    val phase = Random.nextInt(15)
    List.tabulate(experienceSpanOfTime)(t =>
      mySine(A = amplitude, P = period, t = t, shift = shift, phase = phase)
    )
  }

  val sineIterator: Iterator[Double] = Iterator.continually(sineValues).flatten

  def generate(): Double = this.sineIterator.next
}

class IntensityValueGenerator extends SineValueGenerator(25, 0) {
  override val amplitude: Int = 25
  override val shift = 0
}

class PowerValueGenerator extends SineValueGenerator(45, 120) {
  override val amplitude: Int = 45
  override val shift = 120
}

class QuantityValueGenerator extends SineValueGenerator(-3, 0) {
  override val amplitude: Int = -3
  override val shift = 0
}