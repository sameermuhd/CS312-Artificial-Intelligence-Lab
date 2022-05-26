#include "Othello.h"
#include "OthelloBoard.h"
#include "OthelloPlayer.h"
#include <cstdlib>
#include <chrono>
#include <climits>
#include <cmath>

using namespace std;
using namespace Desdemona;

auto start = chrono::steady_clock::now();

int functionNumber = 100;

class MyBot: public OthelloPlayer
{
    public:
        /**
         * Initialisation routines here
         * This could do anything from open up a cache of "best moves" to
         * spawning a background processing thread. 
         */
        MyBot( Turn turn );

        /**
         * Play something 
         */
        virtual Move play( const OthelloBoard& board );
    private:
};

MyBot::MyBot( Turn turn )
    : OthelloPlayer( turn )
{
}

int coinParity(OthelloBoard& board, Turn turn){
    int redCoins = board.getRedCount();
    int blackCoins = board.getBlackCount();

    double coinParity = 100 * ((double)(blackCoins - redCoins) / (double)(blackCoins + redCoins + 1));

    if(turn == BLACK)
        coinParity = 1 * coinParity;
    else
        coinParity = -1 * coinParity;
    
    return round(coinParity);
}

int mobility(OthelloBoard& board, Turn turn){
    int maxPossibleMoves = (board.getValidMoves(turn)).size();
    int minPossibleMoves = (board.getValidMoves(other(turn))).size();

    double currentMobility = 100 * ((double)(maxPossibleMoves - minPossibleMoves) / (double)(maxPossibleMoves + minPossibleMoves));
    currentMobility = 100 * ((currentMobility+ 100) / 200.00);
    return round(currentMobility);
}

int cornerOccupancy(OthelloBoard& board, Turn turn){
    int maxCoins = 0;
    int minCoins = 0;

    for(int x = 0; x < 8; x += 7){
        for(int y = 0; y < 8; y += 7){
            Turn pos = board.get(x, y);
            if(pos == turn) 
                maxCoins += 1;
            else if(pos == other(turn))
                minCoins += 1;
        }
    }
    
    double currentCO = 100 * ((double)(maxCoins - minCoins) / (double)(maxCoins + minCoins));
    currentCO = 100 * ((currentCO + 100) / 200.00);
    return round(currentCO);
}

int positionalScore(OthelloBoard& board, Turn turn){
    int pScore = 0;
    int score[8][8] = {
        {20, -3, 11, 8, 8, 11, -3, 20},
        {-3, -7, -4, 1, 1, -4, -7, -3},
        {11, -4, 2, 2, 2, 2, -4, 11},
        {8, 1, 2, -3, -3, 2, 1, 8},
        {8, 1, 2, -3, -3, 2, 1, 8},
        {11, -4, 2, 2, 2, 2, -4, 11},
        {-3, -7, -4, 1, 1, -4, -7, -3},
        {20, -3, 11, 8, 8, 11, -3, 20},
    };

    for(int x = 0; x < 8; x++){
        for(int y = 0; y < 8; y++){
            Turn pos = board.get(x, y);
            if(pos == turn)
                pScore += score[x][y];
            else if(pos == other(turn))
                pScore -= score[x][y]; 
        }
    }
    double finalScore = 100 * ((double)(pScore + 96) / (double) 360);
    return finalScore;
}

int compositeEvalA(OthelloBoard& board, bool maxPlayer, Turn turn){
    
    Turn maxPlayerTurn;
    if(maxPlayer)
        maxPlayerTurn = turn;
    else
        maxPlayerTurn = other(turn);

    int eval = 0;
    OthelloBoard interBoard = board;

    eval += 10000 * cornerOccupancy(interBoard, maxPlayerTurn);

    int playsDone = interBoard.getRedCount() + interBoard.getBlackCount();
    
    if(playsDone <= 21){
        eval += 30 * positionalScore(interBoard, maxPlayerTurn);
        eval += 30 * mobility(interBoard, turn);
    }
    else if(playsDone <= 42){
        eval += 10 * coinParity(interBoard, maxPlayerTurn);
        eval += 30 * mobility(interBoard, turn);
        eval += 20 * positionalScore(interBoard, maxPlayerTurn);
    }
    else{
        eval += 60 * coinParity(interBoard, maxPlayerTurn);
    }

    return -1 * eval;
}

int compositeEvalB(OthelloBoard& board, bool maxPlayer, Turn turn){
    
    Turn maxPlayerTurn;
    if(maxPlayer)
        maxPlayerTurn = turn;
    else
        maxPlayerTurn = other(turn);

    int eval = 0;
    OthelloBoard interBoard = board;

    int playsDone = interBoard.getRedCount() + interBoard.getBlackCount();

    if(playsDone <= 42){
        eval += 10 * coinParity(interBoard, maxPlayerTurn);
        eval += 30 * mobility(interBoard, turn);
    }
    else{
        eval += 40 * coinParity(interBoard, maxPlayerTurn);
    }

    return -1 * eval;
}

string turnToString(Turn turn){
    if(turn == BLACK){
        return "BLACK";
    }
    else if(turn == RED){
        return "RED";
    }
    return "";
}

int MinMaxAlgo(OthelloBoard board, int depth, Turn turn, bool maxPlayer, int parentID){
    functionNumber += 1;
    if(chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now() - start).count() > 1900){
        return INT_MIN;
    }

    if(depth == 0){
        return compositeEvalA(board, maxPlayer, turn);
    }

    if(maxPlayer){
        int bestEval = INT_MIN + 1;

        list<Move> possibleMoves = board.getValidMoves(turn);

        for(Move currentMove : possibleMoves){
            OthelloBoard interBoard = board;
            interBoard.makeMove(turn, currentMove);

            /*printf("\n[START Explore children of MOVE (%d, %d)  by %s at Depth %d, nodeID: %d, parentID: %d]\n", \
                currentMove.x, currentMove.y, turnToString(turn).c_str(), depth, functionNumber, parentID);*/
            
            int returnVal = MinMaxAlgo(interBoard, depth - 1, other(turn), false, functionNumber);
            if(returnVal == INT_MIN){
                return INT_MIN;
            }

            bestEval = max(returnVal, bestEval);

            /*printf("\n[END Explore children of MOVE (%d, %d)  by %s at Depth %d, nodeID: %d, parentID: %d, Eval: %d, bestEval: %d]\n", \
                currentMove.x, currentMove.y, turnToString(turn).c_str(), depth, functionNumber, parentID, returnVal, bestEval);*/
            
        }
        return bestEval;
    }
    else{
        int bestEval = INT_MAX - 1;

        list<Move> possibleMoves = board.getValidMoves(turn);

        for(Move currentMove : possibleMoves){
            OthelloBoard interBoard = board;
            interBoard.makeMove(turn, currentMove);

            /*printf("\n[START Explore children of MOVE (%d, %d)  by %s at Depth %d, nodeID: %d, parentID: %d]\n", \
                currentMove.x, currentMove.y, turnToString(turn).c_str(), depth, functionNumber, parentID);*/
            
            int returnVal = MinMaxAlgo(interBoard, depth - 1, other(turn), true, functionNumber);

            bestEval = min(returnVal, bestEval);

            /*printf("\n[END Explore children of MOVE (%d, %d)  by %s at Depth %d, nodeID: %d, parentID: %d, Eval: %d, bestEval: %d]\n", \
                currentMove.x, currentMove.y, turnToString(turn).c_str(), depth, functionNumber, parentID, returnVal, bestEval);*/
            
        }
        return bestEval;
    }
}

Move MyBot::play( const OthelloBoard& board )
{   
    functionNumber += 1;

    start = chrono::steady_clock::now();

    list<Move> possibleMoves = board.getValidMoves(turn);
    
    Move bestMove = *(possibleMoves.begin());
    int bestMoveEval = INT_MIN + 1;
    int returnVal = INT_MIN + 1;

    int min_depth = 3;
    int max_depth = 10;

    //printf("\n[START] Root ID: %d\n", functionNumber);

    for(int depth = min_depth; depth <= max_depth; depth++){
        for (Move nextMove : possibleMoves){
            OthelloBoard currentBoard = board;

            currentBoard.makeMove(turn, nextMove);

            returnVal = MinMaxAlgo(currentBoard, depth, other(turn), true, functionNumber);

            if(returnVal == INT_MIN){
                return bestMove;
            }

            if(returnVal > bestMoveEval){
                bestMove = nextMove;
                bestMoveEval = returnVal;

            }
        }
    }

    return bestMove;
}

// The following lines are _very_ important to create a bot module for Desdemona

extern "C" {
    OthelloPlayer* createBot( Turn turn )
    {
        return new MyBot( turn );
    }

    void destroyBot( OthelloPlayer* bot )
    {
        delete bot;
    }
}

