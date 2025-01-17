import System.IO
import Data.Bits
import qualified Data.Map as Map

main = do
    inputFile <- openFile "2018/inputs/day_16_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let (samples, actualCode') = keepTaking inputLines []
    let actualCode = map (map read . words) actualCode'
    let rightVariableOperations = map (, [False], [False, True]) [(+), (*), (.&.), (.|.)]
    let dualVariableOperations = map (, [False, True], [False, True]) [(boolToInt .) . (>), (boolToInt .) . (==)]
    let allOperations' = (leftId, [False, True], [False]):rightVariableOperations ++ dualVariableOperations
    let allOperations = concatMap (\(operation, variableA, variableB) -> [(operation, x, y) | x <- variableA, y <- variableB, not $ x && y]) allOperations'
    print $ sum $ map (\(start, instruction, end) -> atLeast3 [end == applyOperation start instruction operation | operation <- allOperations]) samples
    let possibleOpCodes = Map.fromList [(x, allOperations) | x <- [0..15]]
    let actualOpCodes = deduceAgain $ foldl deduce possibleOpCodes samples
    print $ head $ foldl (\registers instruction -> applyOperation registers instruction (head $ actualOpCodes Map.! head instruction)) (replicate 4 0) actualCode
    putStrLn "done!"

deduce possible (start, instruction, end) = Map.adjust (filter (\operation -> end == applyOperation start instruction operation)) (head instruction) possible

deduceAgain possible
    | all ((1 == ) . length) $ Map.elems possible = possible
    | otherwise = deduceAgain $ Map.map (\operations -> if length operations == 1 then operations else filter (\operation -> convert operation `notElem` assigned) operations) possible
    where assigned = [convert (head x) | x <- Map.elems possible, length x == 1]

keepTaking currentInput runningOutput
    | null $ head currentInput = (runningOutput, tail $ tail currentInput)
    | otherwise = keepTaking (drop 4 currentInput) ((readQuad $ head currentInput, map read $ words $ currentInput !! 1, readQuad $ currentInput !! 2):runningOutput)

readQuad x = map (\y -> read [y]) [x !! 9, x !! 12, x !! 15, x !! 18] :: [Int]

mutateList x position value = take position x ++ (value : drop (position + 1) x)

applyOperation registers [_, inputA, inputB, output] (f, isImmediateA, isImmediateB) = mutateList registers output $ f valueA valueB
    where valueA = if isImmediateA then inputA else registers !! inputA
          valueB = if isImmediateB then inputB else registers !! inputB

boolToInt x = if x then 1 else 0

leftId x _ = x

atLeast3 = flip atLeast3' 0

atLeast3' _ 3 = 1
atLeast3' [] _ = 0
atLeast3' (x:xs) count = atLeast3' xs (count + if x then 1 else 0)

detector f = case f 10 6 of
    0  -> "="
    14 -> "|"
    2  -> "&"
    16 -> "+"
    60 -> "*"
    1  -> ">"
    10 -> "I"

convert (f, a, b) = detector f ++ (if a then "i" else "r") ++ if b then "i" else "r"
