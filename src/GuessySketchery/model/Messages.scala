package GuessySketchery.model

case object SendGameState
case class GameState(gameState: String)

case class AddPlayer(username: String)
case class RemovePlayer(username: String)
case class MouseDraw(username: String)
