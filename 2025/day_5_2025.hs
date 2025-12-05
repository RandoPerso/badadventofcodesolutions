import System.IO
import qualified Data.List as List
import Data.Ord

main = do
    inputFile <- openFile "2025/inputs/day_5_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let ranges = getIds [] $ takeWhile (/= "") inputLines
    print $ countThem ranges 0 $ tail $ dropWhile (/= "") inputLines
    let ranges2 = List.sortBy (comparing fst) ranges
    print $ countThem2 0 (-999) ranges2
    putStrLn "done!"

getIds output (x:xs) = getIds ((a, b):output) xs
    where a :: Integer = read $ takeWhile (/= '-') x 
          b :: Integer = read $ tail $ dropWhile (/= '-') x
getIds output [] = output

countThem ranges output (x:xs)
    | inRange ranges a = countThem ranges (output + 1) xs 
    | otherwise = countThem ranges output xs
    where a :: Integer = read x
countThem _ output [] = output

inRange ranges a = any (\(x, y) -> a >= x && a <= y) ranges

countThem2 output last (x@(a, b):xs)
    | last >= snd x = countThem2 output last xs
    | last >= fst x = countThem2 (output + b - last) (snd x) xs
    | otherwise = countThem2 (output + b - a + 1) (snd x) xs
countThem2 output _ [] = output
