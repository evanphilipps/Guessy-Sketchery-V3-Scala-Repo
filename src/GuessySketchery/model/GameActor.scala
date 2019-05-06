package GuessySketchery.model

import akka.actor.{Actor, ActorRef, PoisonPill, Props}

case object UpdateGame

class GameActor extends Actor {

  var players: Map[String, ActorRef] = Map()
  val game: Game = new Game()


  override def receive: Receive = {
    case message: AddPlayer => game.addPlayer(message.username)
    case message: RemovePlayer => game.removePlayer(message.username)
    case message: MouseDraw => game.drawings(message.username)
    case UpdateGame =>
    case SendGameState => sender() ! GameState(game.gameState())
  }
}