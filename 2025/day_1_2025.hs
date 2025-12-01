import System.IO

main = do
    inputFile <- openFile "2025/inputs/day_1_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    print $ countTimes 0 50 inputLines
    print $ countTimes2 0 50 inputLines
    putStrLn "done!"

countTimes output current (x:xs)
    | newCurr == 0 = countTimes (output+1) newCurr xs
    | otherwise = countTimes output newCurr xs
    where dir = if head x == 'R' then 1 else -1
          amount :: Integer = read $ tail x
          newCurr = (current + dir * amount) `mod` 100
countTimes output _ [] = output

countTimes2 output current (x:xs) = countTimes2 newOut newCurr xs
    where dir = if head x == 'R' then 1 else -1
          amount :: Integer = read $ tail x
          newCurr = (current + dir * amount) `mod` 100
          newOut' = output + (amount `div` 100)
          newAmount = amount `mod` 100
          addAnother = 0 `elem` map (`mod` 100) [current + dir, current + dir * 2..current + dir * newAmount]
          newOut = if addAnother then newOut' + 1 else newOut'
countTimes2 output _ [] = output