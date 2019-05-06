package GuessySketchery.model

import play.api.libs.json.{JsValue, Json}

class Game {

  var players: Map[String, Player] = Map()
  var drawings: Map[String, Double] = Map()
  var lastUpdateTime: Long = System.nanoTime()

  def addPlayer(username: String): Unit = {
    val player = new Player(0, "guesser", "")
    players += (username -> player)
  }

  def removePlayer(username: String): Unit = {
    players -= username
  }

def gameState(): String = {
  val gameState: Map[String, JsValue] = Map(
    "players" -> Json.toJson(this.players.map({ case (k, v) => Json.toJson(Map(
      "score" -> Json.toJson(v.pScore),
      "job" -> Json.toJson(v.pJob),
      "guess" -> Json.toJson(v.pGuess),
      "id" -> Json.toJson(k)))
    })),
    "drawings" -> Json.toJson(drawings))
  Json.stringify(Json.toJson(gameState))
}
/*
  def gameState(): String = {
    val gameState: Map[String, JsValue] = Map(
      "players" -> Json.toJson(this.players.map({ case (k, v) => Json.toJson(Map(
        "username" -> Json.toJson(v.username),
        "score" -> Json.toJson(v.score),
        "job" -> Json.toJson(v.job),
        "guess" -> Json.toJson(v.guess),
        "id" -> Json.toJson(k)))
      }))

    )

    Json.stringify(Json.toJson(gameState))
  }

*/
}

