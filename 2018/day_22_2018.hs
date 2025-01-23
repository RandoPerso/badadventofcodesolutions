import System.IO

main = do
    inputFile <- openFile "2018/inputs/day_22_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let [inputDepth, inputTarget] = lines contents
    let depth = read $ drop 7 inputDepth :: Integer
    let (targetX', targetY') = break (== ',') $ drop 8 inputTarget
    let (targetX, targetY) = (read targetX', read $ tail targetY') :: (Integer, Integer)
    let initialList = [(16807 * x) `mod` 60549 | x <- [1..targetX]]
    print $ createSum depth 1 targetY initialList (getType depth 0 + sum (map (getType depth) initialList))
    putStrLn "done!"

noMod a _ = a

createSum depth yCoordinate maxY currentRow currentSum
    | yCoordinate > maxY = currentSum - getType depth (last currentRow) + getType depth 0
    | otherwise = createSum depth (yCoordinate + 1) maxY nextRow (currentSum + getType depth nextInitial + sum (map (getType depth) nextRow))
    where nextInitial = (yCoordinate * 48271) `mod` 60549
          nextRow = getNextRow depth nextInitial currentRow

getNextRow _ _ [] = []
getNextRow depth previous (x:xs) = nextScore : getNextRow depth nextScore xs
    where nextScore = (getErosion depth previous * getErosion depth x) `mod` 60549

getErosion depth x = (x + depth) `mod` 20183

getType  = ((`mod` 3) .) . getErosion
