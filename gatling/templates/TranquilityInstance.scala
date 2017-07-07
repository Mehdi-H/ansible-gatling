/**
  * Created by mho on 05/05/17.
  */
class TranquilityInstance extends AbstractTranquility{
  val protocol = "http"
  val host = "{{ target.host }}"
  val port = "{{ target.port }}"
  val dataSource = "test-constant-signal"
  val requestPath = "/v1/post/" + this.dataSource
  val url = this.protocol + "://" + this.host + ":" + this.port
  val fullUrl: String = this.url + this.requestPath
}
