#include <iostream>
#include <algorithm>
#include "fast_ai.h"
#include <boost/python.hpp>
#include <boost/python/call.hpp>
#include <boost/python/list.hpp>

namespace {
    const char BOARD_LENGTH = 9;
    const short MAX_INIT = -1000;
    const short MIN_INIT = 1000;
    const short MIN_VICTORY = -10;
    const short MAX_VICTORY = 10;
    const short DRAW_SCORE = 0;
    
    enum EvaluationValue { PLAYER_1, PLAYER_2, DRAW, ONGOING };

    struct Move {
        char position;
        short score;
    };

    struct AiConfig {
        char player1;
        char player2;
        char emptyValue;
    };
    
    class MinMaxAi {
        public:
            MinMaxAi(AiConfig config) {
                aiconfig = config;
            };
            
            int getPlayerMove(char player, boost::python::list& gameBoard) {
                srand(time(NULL));
                maxPlayer = player;
                board = gameBoard;
                short bestScore = MAX_INIT;
                Move bestMoves[BOARD_LENGTH] = {};
                char bestMovesCount = 0;

                for (int i = 0; i < BOARD_LENGTH; i++) {
                    // Check if the tile is empty
                    char tile = boost::python::extract<char>(board[i]);
                    if (tile == aiconfig.emptyValue) {
                        // Do the move
                        board[i] = player;
                        // Check the move score
                        short score = minmax(player, 0, MAX_INIT, MIN_INIT);
                        // Undo the move
                        board[i] = aiconfig.emptyValue;
                        // Check if it's a better move
                        if (score > bestScore) {
                            bestScore = score;
                            memset(bestMoves, 0, sizeof(bestMoves));
                            Move move;
                            move.position = i;
                            move.score = bestScore;
                            bestMoves[0] = move;
                            bestMovesCount = 1;
                        } else if (score == bestScore) {
                            Move move;
                            move.position = i;
                            move.score = bestScore;
                            bestMoves[bestMovesCount] = move;
                            bestMovesCount++; 
                        }
                    }
                }
                if (bestMovesCount == 0) {
                    return -1;
                }
                short moveIdx = rand() % bestMovesCount;
                Move selectedMove = bestMoves[moveIdx];

                return selectedMove.position;
            };
        private:
            AiConfig aiconfig;
            char maxPlayer;
            boost::python::list board;

            char getOpponentPlayer(char player) {
                return aiconfig.player1 == player ? aiconfig.player2 : aiconfig.player1;
            };

            short minmax(char player, short depth, short alpha, short beta) {
                EvaluationValue evaluation = evaluateBoard(aiconfig.player1, aiconfig.player2, aiconfig.emptyValue);

                // Check player 1 victory
                if (evaluation == EvaluationValue::PLAYER_1) {
                    short score = (maxPlayer == aiconfig.player1) ? MAX_VICTORY - depth : MIN_VICTORY + depth;
                }
                // Check player 2 victory
                if (evaluation == EvaluationValue::PLAYER_2) {
                    return (maxPlayer == aiconfig.player2) ? MAX_VICTORY - depth : MIN_VICTORY + depth;
                }
                // Check draw:
                if (evaluation == EvaluationValue::DRAW) {
                    short score = DRAW_SCORE + depth;
                    if (player == maxPlayer) {
                        score *= -1;
                    }
                    return score;
                }
                if (maxPlayer == player) {
                    // Process minmax if MAX turn
                    short bestScore = MAX_INIT;
                    for (short i = 0; i < BOARD_LENGTH; i++) {
                        char tile = boost::python::extract<char>(board[i]);
                        if (tile == aiconfig.emptyValue) {
                            // Do the move
                            board[i] = player;
                            bestScore = std::max(minmax(getOpponentPlayer(player), ++depth, alpha, beta), bestScore);
                            // Undo the move
                            board[i] = aiconfig.emptyValue;
                            // Prunning
                            alpha = std::max(bestScore, alpha);
                            if (beta <= alpha) {
                                break;
                            }
                        }
                    }
                    return bestScore;
                } else {
                    // Process minmax if MIN player
                    short bestScore = MIN_INIT;
                    for (short i = 0; i < BOARD_LENGTH; i++) {
                        char tile = boost::python::extract<char>(board[i]);
                        if (tile == aiconfig.emptyValue) {
                            // Do the move
                            board[i] = player;
                            bestScore = std::min(minmax(getOpponentPlayer(player), ++depth, alpha, beta), bestScore);
                            // Undo the move
                            board[i] = aiconfig.emptyValue;
                            // Prunning
                            beta = std::min(bestScore, beta);
                            if (beta <= alpha) {
                                break;
                            }
                        }
                    }
                    return bestScore;
                }
            };

            void printBoard() {
                for (int i = 0; i < BOARD_LENGTH; i++) {
                    char tile = boost::python::extract<char>(board[i]);
                    printf("%c ", tile);
                }
                printf("\n");
            }

            EvaluationValue evaluateBoard(char player1, char player2, char emptyTile) {
                // check lines victory
                // printBoard();
                for (int i = 0; i < 3; i++) {
                    int idx = i*3;
                    char tile1 = boost::python::extract<char>(board[idx]);
                    char tile2 = boost::python::extract<char>(board[idx + 1]);
                    char tile3 = boost::python::extract<char>(board[idx + 2]);
                    if ((tile1 == tile2) && (tile2 == tile3) && (tile1 != emptyTile)) {
                        return tile1 == player1 ? EvaluationValue::PLAYER_1 : EvaluationValue::PLAYER_2;
                    }
                }
                // Check columns victory
                for (int i = 0; i < 3; i++) {
                    char tile1 = boost::python::extract<char>(board[i]);
                    char tile2 = boost::python::extract<char>(board[i + 3]);
                    char tile3 = boost::python::extract<char>(board[i + 6]);
                    if ((tile1 == tile2) && (tile2 == tile3) && (tile1 != emptyTile)) {
                        return tile1 == player1 ? EvaluationValue::PLAYER_1 : EvaluationValue::PLAYER_2;
                    }
                }
                // Check diagonal victory
                char tile1 = boost::python::extract<char>(board[0]);
                char tile2 = boost::python::extract<char>(board[5]);
                char tile3 = boost::python::extract<char>(board[8]);
                if ((tile1 == tile2) && (tile2 == tile3) && (tile1 != emptyTile)) {
                    return tile1 == player1 ? EvaluationValue::PLAYER_1 : EvaluationValue::PLAYER_2;
                }
                tile1 = boost::python::extract<char>(board[2]);
                tile2 = boost::python::extract<char>(board[5]);
                tile3 = boost::python::extract<char>(board[6]);
                if ((tile1 == tile2) && (tile2 == tile3) && (tile1 != emptyTile)) {
                    return tile1 == player1 ? EvaluationValue::PLAYER_1 : EvaluationValue::PLAYER_2;
                }

                // Check DRAW
                bool isDraw = true;
                for (int i = 0; i < BOARD_LENGTH; i++) {
                    if (board[i] == emptyTile) {
                        isDraw = false;
                        break;
                    }
                }
                if (isDraw) {
                    return EvaluationValue::DRAW;
                }

                // If any condition applies, game is ongoing
                return EvaluationValue::ONGOING;
            };

            
    };
}

BOOST_PYTHON_MODULE(fast_ai)
{
    using namespace boost::python;
    
    class_<AiConfig>("AiConfig")
        .def_readwrite("player1", &AiConfig::player1)
        .def_readwrite("player2", &AiConfig::player2)
        .def_readwrite("emptyValue", &AiConfig::emptyValue);

    class_<MinMaxAi>("MinMaxAi", init<AiConfig&>())
        .def("getPlayerMove", &MinMaxAi::getPlayerMove);
}
