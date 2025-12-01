import System.IO

main = do
    inputFile <- openFile "2016/inputs/day_2_2016.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let output = foldl (\a b -> a ++ doMoves b (1, 1)) "" inputLines
    print output
    let output' = foldl (\a b -> a ++ doMoves' b (0, 2)) "" inputLines
    print output'
    putStrLn "done!"

doMoves [] (x, y) = show $ x + 3 * y + 1
doMoves (move:xs) position@(x, y)
    | inBounds newPosition = doMoves xs newPosition
    | otherwise = doMoves xs position
    where (dirX, dirY) = getDirection move
          newPosition@(newX, newY) = (x + dirX, y + dirY)

getDirection letter
    | letter == 'L' = (-1, 0)
    | letter == 'R' = (1, 0)
    | letter == 'D' = (0, 1)
    | letter == 'U' = (0, -1) 

inBounds (x, y) = (x >= 0 && x < 3) && (y >= 0 && y < 3)

doMoves' [] position = case position of
    (2, 0) -> "1"
    (1, 1) -> "2"
    (2, 1) -> "3"
    (3, 1) -> "4"
    (0, 2) -> "5"
    (1, 2) -> "6"
    (2, 2) -> "7"
    (3, 2) -> "8"
    (4, 2) -> "9"
    (1, 3) -> "A"
    (2, 3) -> "B"
    (3, 3) -> "C"
    (2, 4) -> "D"

doMoves' (move:xs) position@(x, y)
    | inBounds' newPosition = doMoves' xs newPosition
    | otherwise = doMoves' xs position
    where (dirX, dirY) = getDirection move
          newPosition@(newX, newY) = (x + dirX, y + dirY)


inBounds' position = position `elem` [(2, 0), (1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (1, 3), (2, 3), (3, 3), (2, 4)]
