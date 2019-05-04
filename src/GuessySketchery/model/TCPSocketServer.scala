package GuessySketchery.model
import java.net.InetSocketAddress

import akka.actor.{Actor, ActorRef, ActorSystem, Props}
import akka.io.{IO, Tcp}
import play.api.libs.json.{JsValue, Json}



class TCPSocketServer(gameActor: ActorRef) extends Actor {

  import Tcp._
  import context.system

  IO(Tcp) ! Bind(self, new InetSocketAddress("localhost", 8000))

  var webServers: Set[ActorRef] = Set()
  var buffer: String = ""
  val delimiter: String = "~"

  override def receive: Receive = {
    case b: Bound => println("Listening on port: " + b.localAddress.getPort)
    case c: Connected =>
      println("Client Connected: " + c.remoteAddress)
      this.webServers = this.webServers + sender()
      sender() ! Register(self)
      println()

  }

  def handleMessageFromWebServer(messageString: String): Unit = {
    val message: JsValue = Json.parse(messageString)
    val username = (message \ "username").as[String]
    val messageType = (message \ "action").as[String]

    messageType match {
      case "connected" => gameActor ! AddPlayer(username)
      case "disconnected" => gameActor ! RemovePlayer(username)
    }
  }
}

  object TCPSocketServer {

    def main(args: Array[String]): Unit = {
      val actorSystem = ActorSystem()

      val gameActor = actorSystem.actorOf(Props(classOf[GameActor]))
      val server = actorSystem.actorOf(Props(classOf[TCPSocketServer], gameActor))

      //actorSystem.scheduler.schedule(16.milliseconds, 32.milliseconds, gameActor, UpdateGame)
      // actorSystem.scheduler.schedule(32.milliseconds, 32.milliseconds, server, SendGameState)
    }

  }


