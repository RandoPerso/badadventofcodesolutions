import System.IO

main = do
    inputFile <- openFile "2025/inputs/day_6_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let (numbers, ops) = getNumbers (replicate (length $ words $ head inputLines) []) inputLines
    print $ getTotal 0 numbers ops
    let temp = reflect (replicate (length $ head inputLines) []) inputLines ++ [" "]
    print $ getThing 0 temp ops
    putStrLn "done!"

getNumbers output [x] = (output, words x)
getNumbers output (x:xs) = getNumbers (doubleZip output y) xs
    where y :: [Integer] = map read $ words x

doubleZip (x:xs) (y:ys) = (y:x):doubleZip xs ys
doubleZip [] [] = []

doubleZip' (x:xs) (y:ys) = (y:x):doubleZip' xs ys
doubleZip' (x:xs) [] = (' ':x):doubleZip' xs []
doubleZip' [] [] = []

getTotal output [] [] = output
getTotal output (x:xs) (y:ys) = getTotal newOut xs ys
    where newOut = if y == "*" then output + product x else output + sum x

reflect output [] = map reverse output
reflect output (x:xs) = reflect (doubleZip' output x) xs

getThing output x [] = output
getThing output x (y:ys)
    | y == "*" = getThing2 output x ys 1 (*)
    | otherwise = getThing2 output x ys 0 (+)

getThing2 output (x:xs) ys rolling op
    | all (== ' ') x = getThing (output + rolling) xs ys
    | otherwise = getThing2 output xs ys (op rolling (read $ clean x)) op


clean x
    | last x == '*' || last x == '+' = init x
    | otherwise = x
