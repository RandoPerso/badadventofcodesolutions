import System.IO

main = do
    inputFile <- openFile "2017/inputs/day_1_2017.txt" ReadMode
    contents <- hGetContents inputFile
    print $ getSum contents 0 + if last contents == head contents then read [head contents] else 0
    print $ getSum2 contents

getSum (a:xs) total
    | length xs == 1 = total
    | a == head xs = getSum xs (total + read [a])
    | otherwise = getSum xs total

getSum2 x = foldl (\a b -> if x !! b == x !! ((length x `div` 2 + b) `mod` length x) then a + read [x !! b] else a) 0 [0..length x - 1]