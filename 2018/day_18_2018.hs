import System.IO
import Data.List
import qualified Data.Map as Map
import Data.Maybe

main = do
    inputFile <- openFile "2018/inputs/day_18_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let maxY = length inputLines - 1
    let maxX = length (head inputLines) - 1
    let inputMap = listToMap inputLines
    let iterations = iterate nextIteration inputMap
    print $ getScore 0 0 $ Map.elems $ iterations !! 10
    -- let allScores = map (show . getScore 0 0 . Map.elems) iterations
    -- writeFile "temp.txt" $ unlines $ take 1000 allScores
    let indexedIterations = enumerate iterations
    let (loopStart, loopLength) = findLoop indexedIterations
    putStrLn "This will take a bit..."
    print $ getScore 0 0 $ Map.elems $ iterations !! ((1000000000 - loopStart) `mod` loopLength + loopStart)
    putStrLn "done!"

findLoop = findLoop' []
findLoop' visited (x@(index, nextPosition):otherPositions)
    | isJust location' = (index, index - oldIndex)
    | otherwise = findLoop' (x:visited) otherPositions
    where location' = find ((== nextPosition) . snd) visited
          (oldIndex, _) = fromJust location'

nextIteration m = Map.mapWithKey (\location char -> let neighbors = map (`safeLookup` m) (spreadOut location) in case char of
        '.' -> if atLeast3 '|' neighbors then '|' else '.'
        '|' -> if atLeast3 '#' neighbors then '#' else '|'
        '#' -> if elem '#' neighbors && elem '|' neighbors then '#' else '.'
    ) m

getScore lumber trees [] = lumber * trees
getScore lumber trees (x:xs) = case x of 
    '.' -> getScore lumber trees xs
    '|' -> getScore lumber (trees + 1) xs
    '#' -> getScore (lumber + 1) trees xs

safeLookup = (fromMaybe '.' .) . Map.lookup

tupAdd (x1, y1) (x2, y2) = (x1 + x2, y1 + y2)

spreadOut x = map (tupAdd x) [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]

atLeast3 = atLeast3' 0
atLeast3' 3 _ _ = True
atLeast3' _ _ [] = False
atLeast3' counter searching (x:xs)
    | searching == x = atLeast3' (counter + 1) searching xs
    | otherwise = atLeast3' counter searching xs

listToMap m = Map.fromList [((x, y), char) | (y, line) <- enumerate m, (x, char) <- enumerate line]

enumerate = zip [0..]

displayMap maxY maxX m = unlines [[m Map.! (x, y) | x <- [0..maxX]] | y <- [0..maxY]]
