import System.IO

main = do
    inputFile <- openFile "2018/inputs/day_10_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let parsedInput = map parse inputLines
    let (message, time) = moveUntilSmall parsedInput
    putStrLn $ display message
    print time
    putStrLn "done!"

parse :: [Char] -> ([Int], [Int])
parse x = (map read $ wordsBy ',' $ takeWhile (/= '>') $ tail $ dropWhile (/= '<') x, map read $ wordsBy ',' $ takeWhile (/= '>') $ tail $ tail $ tail $ dropWhile (/= 'y') x)

wordsBy separator x =  case dropWhile (== separator) x of
                         "" -> []
                         s' -> w : wordsBy separator s''
                             where (w, s'') = break (== separator) s'

boundingBox x = (minimum xCoors, maximum xCoors, minimum yCoors, maximum yCoors)
    where locations = map fst x
          xCoors = map head locations
          yCoors = map last locations

area (minX, maxX, minY, maxY) = (maxX - minX) * (maxY-minY)

display x = unlines $ [[if [x, y] `elem` locations then '#' else '.' | x <- [minX..maxX]] | y <- [minY..maxY]]
    where locations = map fst x
          (minX, maxX, minY, maxY) = boundingBox x

move (location, velocity) = (zipWith (+) location velocity, velocity)

moveUntilSmall x = moveUntilSmall' x 0

moveUntilSmall' x timer
    | nextArea > currentArea = (x, timer)
    | otherwise = moveUntilSmall' nextState (timer + 1)
    where currentArea = area $ boundingBox x
          nextState = map move x
          nextArea = area $ boundingBox nextState
