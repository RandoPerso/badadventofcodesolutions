import System.IO
import Data.List
import Data.Function
import qualified Data.Map as Map
import Data.Maybe

main = do
    inputFile <- openFile "2018/inputs/day_11_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let serialNumber = read contents :: Int
    let powerMap = Map.fromList [((x, y), calculate serialNumber (x, y)) | x <- [1..300], y <- [1..300]]
    let horizontalSums = Map.fromList $ concat [scanl (\((x, y), total) next -> ((x + 1, y), total + next)) ((1, y), 0) [getFromMap (x, y) powerMap | x <- [1..300]] | y <- [1..300]] 
    let verticalSums = Map.fromList $ concat [scanl (\((x, y), total) next -> ((x, y + 1), total + next)) ((x, 1), 0) [getFromMap (x, y) powerMap | y <- [1..300]] | x <- [1..300]] 
    let bestSquare'' = bestSquare' powerMap horizontalSums verticalSums
    print $ fst $ maximumBy (compare `on` snd) [((x, y), sum $ [getFromMap (x + a, y + b) powerMap | a <- [0 .. 2], b <- [0 .. 2]]) | x <- [1..298], y <- [1..298]]
    putStrLn "This might take a bit..."
    -- print $ maximumBy (compare `on` snd) [bestSquare'' (x, y) 0 0 ((0, 0, 0), 0) 2 | x <- [1..298], y <- [1..298]]
    let bestSquare (x, y) = bestSquare'' (x, y) 0 0 ((0, 0, 0), 0) (300 - max x y)
    print $ fst $ maximumBy (compare `on` snd) [bestSquare (x, y) | x <- [1..300], y <- [1..300]]
    putStrLn "done!"

calculate serialNumber (x, y) = (((rackID * (rackID * y + serialNumber)) `div` 100) `mod` 10) - 5
    where rackID = x + 10

{-
bestSquare' powerMap (x, y) size current best maxSize
    | size > maxSize = best
    | otherwise = bestSquare' powerMap (x, y) (size + 1) next nextBest maxSize
    where next = current + sum [fromJust $ Map.lookup (x + size, y + a) powerMap | a <- [0..size]] + sum [fromJust $ Map.lookup (x + a, y + size) powerMap | a <- [0..(size - 1)]]
          nextBest = if snd best < next then ((x, y, size + 1), next) else best
-}

getFromMap key map = fromJust $ Map.lookup key map

bestSquare' powerMap horizontalSums verticalSums (x, y) size current best maxSize
    | size > maxSize = best
    | otherwise = bestSquare' powerMap horizontalSums verticalSums (x, y) (size + 1) next nextBest maxSize
    where next = current + getFromMap (x + size, y + size + 1) verticalSums - getFromMap (x + size, y) verticalSums + getFromMap (x + size, y + size) horizontalSums - getFromMap (x, y + size) horizontalSums
          nextBest = if snd best < next then ((x, y, size + 1), next) else best
