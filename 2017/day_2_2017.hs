import System.IO
import Data.Maybe
import Data.List

main = do
    inputFile <- openFile "2017/inputs/day_2_2017.txt" ReadMode
    contents <- hGetContents inputFile
    print $ getChecksum contents
    print $ getDivisons contents

getChecksum = sum . map getRowDifference . lines
getRowDifference row = maximum numbers - minimum numbers
    where numbers = map read $ words row

getDivisons = sum . map getRowDivision . lines
getRowDivision row = getRowDivision' numbers numbers
    where numbers = map read $ words row

getRowDivision' (x:xs) full
    | isJust result = fromJust result `div` x
    | otherwise = getRowDivision' xs full
    where result = find (\a -> a > x && a `mod` x == 0) full
