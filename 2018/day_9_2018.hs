import System.IO
import Data.List
import qualified Data.Map as Map
import Data.Maybe

-- WARNING: THIS CODE WILL USE A TON OF MEMORY AND PROBABLY CRASH YOUR COMPUTER
-- YOU HAVE BEEN WARNED

main = do
    putStrLn "read the warning."
    {-
    inputFile <- openFile "2018/inputs/day_9_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let (numPlayers, numPoints) = (\x -> (read $ head x, read $ x !! 6)) $ words contents :: (Int, Int)
    let _ = print $ fasterFindScore numPlayers numPoints
    let _ = print $ fasterFindScore numPlayers (numPoints * 100)
    putStrLn "done!"
    -}
        

{-
findScore numPlayers numPoints = findScore' numPlayers numPoints 0 1 [0] (replicate numPlayers 0)

insertAt index item list = take index list ++ (item : drop index list)

deleteAt index list = take index list ++ drop (index + 1) list

editAt index item list = take index list ++ (item : drop (index + 1) list)

findScore' numPlayers numPoints currentBall nextBall circle scores
    | nextBall > numPoints = maximum scores
    | nextBall `mod` 23 == 0 = findScore' numPlayers numPoints removingLocation (nextBall + 1) (deleteAt removingLocation circle) (editAt (nextBall `mod` numPlayers) ((scores !! (nextBall `mod` numPlayers)) + nextBall + (circle !! removingLocation)) scores)
    | otherwise = findScore' numPlayers numPoints nextLocation (nextBall + 1) (insertAt nextLocation nextBall circle) scores
    where nextLocation = (currentBall + 2) `mod` length circle
          removingLocation = (currentBall - 7) `mod` length circle
-}

{-
fasterFindScore numPlayers numPoints = findScore'' numPlayers numPoints 0 1 [0] 1 (Map.fromList [(x,0) | x <- [0..(numPlayers - 1)]])

findScore'' numPlayers numPoints currentBall nextBall circle circleSize scoresMap
    | nextBall > numPoints = maximum $ Map.elems scoresMap
    | nextBall `mod` 23 == 0 = findScore'' numPlayers numPoints removingLocation (nextBall + 1) (deleteAt removingLocation circle) (circleSize - 1) (Map.adjust (\x -> traceShowId (x + nextBall + (circle !! removingLocation))) (nextBall `mod` numPlayers) scoresMap)
    | otherwise = findScore'' numPlayers numPoints nextLocation (nextBall + 1) (insertAt nextLocation nextBall circle) (circleSize + 1) scoresMap
    where nextLocation = (currentBall + 2) `mod` circleSize
          removingLocation = (currentBall - 7) `mod` circleSize
-}

fasterFindScore numPlayers numPoints = findScore'' numPlayers numPoints 0 1 (Map.fromList [(0, (0, 0))]) (Map.fromList [(x,0) | x <- [0..(numPlayers - 1)]])

getFrom :: Int -> Map.Map Int (Int, Int) -> (Int, Int)
getFrom x y = fromJust $ Map.lookup x y

getNext pointer x = next
    where (_, next) = getFrom pointer x

getBack pointer x = back
    where (back, _) = getFrom pointer x

insertAfter pointer value x
    | next == pointer = Map.insert value (pointer, pointer) $ Map.insert pointer (value, value) x
    | otherwise = Map.insert value (pointer, next) $ Map.insert next (value, b) $ Map.insert pointer (a, value) x
    where next = getNext pointer x
          (a, _) = getFrom pointer x
          (_, b) = getFrom next x

removeBack pointer x = Map.insert doubleBack (b, pointer) $ Map.insert pointer (doubleBack, a) $ Map.delete back x
    where (_, a) = getFrom pointer x
          back = getBack pointer x
          doubleBack = getBack back x
          (b, _) = getFrom doubleBack x

loopN f a b 0 = a
loopN f a b n = loopN f (f a b) b (n - 1)

getNextN = loopN getNext
getBackN = loopN getBack

findScore'' numPlayers numPoints currentBall nextBall circle scoresMap
    | nextBall > numPoints = maximum $ Map.elems scoresMap
    | nextBall `mod` 23 == 0 = do
        let !nextSum = nextBall + removalValue + fromJust (Map.lookup (nextBall `mod` numPlayers) scoresMap)
        findScore'' numPlayers numPoints removingLocation (nextBall + 1) (removeBack removingLocation circle) (Map.insert (nextBall `mod` numPlayers) nextSum scoresMap)
    | otherwise = findScore'' numPlayers numPoints nextBall (nextBall + 1) (insertAfter nextLocation nextBall circle) scoresMap
    where nextLocation = getNext currentBall circle
          removingLocation = getBackN currentBall circle 6
          removalValue = getBack removingLocation circle
