import System.IO
import qualified Data.Set as Set
import Data.Maybe

main = do
    inputFile <- openFile "2016/inputs/day_1_2016.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = doSplit contents
    print $ execute inputLines (0, 0) 0
    print $ execute2 inputLines Set.empty (0, 0) 0
    putStrLn "done!"

doSplit = doSplit' [] ""

doSplit' output running [] = reverse (reverse running : output)
doSplit' output running (x:xs)
    | x == ',' = doSplit' (reverse running : output) "" (tail xs)
    | otherwise = doSplit' output (x : running) xs

execute [] (a,b) _ = abs a + abs b
execute (command:xs) position direction = execute xs (doMove position newDirection amount) newDirection
    where turning = head command
          amount :: Int = read $ tail command
          newDirection = if turning == 'L' then (direction - 1) `mod` 4 else (direction + 1) `mod` 4

doMove (x,y) direction amount
    | direction == 0 = (x, y - amount)
    | direction == 1 = (x + amount, y)
    | direction == 2 = (x, y + amount)
    | direction == 3 = (x - amount, y)

doMove2 (x,y) direction amount
    | direction == 0 = ([(x, y - a) | a <- [1..amount]], (x, y - amount))
    | direction == 1 = ([(x + a, y) | a <- [1..amount]], (x + amount, y))
    | direction == 2 = ([(x, y + a) | a <- [1..amount]], (x, y + amount))
    | direction == 3 = ([(x - a, y) | a <- [1..amount]], (x - amount, y))

findFirst [] y = Nothing
findFirst (x:xs) y
    | Set.member x y = Just x
    | otherwise = findFirst xs y

execute2 (command:xs) visited position direction
    | isJust result = abs a + abs b
    | otherwise =  execute2 xs newVisited newPosition newDirection
    where turning = head command
          amount :: Int = read $ tail command
          newDirection = if turning == 'L' then (direction - 1) `mod` 4 else (direction + 1) `mod` 4
          (newPositions, newPosition) = doMove2 position newDirection amount
          setNew = Set.fromList newPositions
          newVisited = Set.union visited setNew
          result = findFirst newPositions visited
          (a,b) = fromJust result

