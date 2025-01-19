import System.IO
import Data.List
import Data.Bits
import qualified Data.Map as Map
import Data.Maybe

main = do
    inputFile <- openFile "2018/inputs/day_19_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let rightVariableOperations = map (, [False], [False, True]) [(+), (*), (.&.), (.|.)] :: [(Int -> Int -> Int, [Bool], [Bool])]
    let dualVariableOperations = map (, [False, True], [False, True]) [(boolToInt .) . (>), (boolToInt .) . (==)]
    let allOperations' = (leftId, [False, True], [False]):rightVariableOperations ++ dualVariableOperations
    let allOperations = concatMap (\(operation, variableA, variableB) -> [(operation, x, y) | x <- variableA, y <- variableB, not $ x && y]) allOperations'
    let operationsMap = Map.fromList $ map (\operation -> (convert operation, operation)) allOperations
    let ipRegister = read [head inputLines !! 4] :: Int
    let instructionsMap = Map.fromList $ zip [0..] $ map (parse operationsMap) $ tail inputLines
    -- print $ doIt ipRegister instructionsMap $ replicate 6 0
    -- print $ doIt ipRegister instructionsMap $ 1 : replicate 5 0
    let startingValue1 = getStartingValue ipRegister instructionsMap $ replicate 6 0
    print $ sum $ getFactors startingValue1
    let startingValue2 = getStartingValue ipRegister instructionsMap $ 1 : replicate 5 0
    print $ sum $ getFactors startingValue2
    putStrLn "done!"

getFactors m = filter (\x -> m `mod` x == 0) [1..m]

{-
doIt ipRegister instructionsMap registers
    | isNothing nextInstruction = head registers
    | otherwise = doIt ipRegister instructionsMap nextState
    where nextInstruction = Map.lookup (registers !! ipRegister) instructionsMap
          nextState' = fromJust nextInstruction registers
          nextIP = (nextState' !! ipRegister) + 1
          nextState = mutateList nextState' ipRegister nextIP
-}

getStartingValue ipRegister instructionsMap registers
    | registers !! ipRegister == 1 = registers !! 1
    | otherwise = getStartingValue ipRegister instructionsMap nextState
    where nextInstruction = Map.lookup (registers !! ipRegister) instructionsMap
          nextState' = fromJust nextInstruction registers
          nextIP = (nextState' !! ipRegister) + 1
          nextState = mutateList nextState' ipRegister nextIP

parse operationsMap line = applyOperation (instruction, a, b, c)
    where [instruction', a', b', c'] = words line
          instruction = operationsMap Map.! instruction'
          [a, b, c] = map read [a', b', c'] :: [Int]

boolToInt x = if x then 1 else 0

leftId x _ = x

mutateList x position value = take position x ++ (value : drop (position + 1) x)

applyOperation ((f, isImmediateA, isImmediateB), inputA, inputB, output) registers = mutateList registers output $ f valueA valueB
    where valueA = if isImmediateA then inputA else registers !! inputA
          valueB = if isImmediateB then inputB else registers !! inputB

detector f = case f 10 6 of
    0  -> "eq"
    14 -> "bor"
    2  -> "ban"
    16 -> "add"
    60 -> "mul"
    1  -> "gt"
    10 -> "set"

convert (f, a, b)
    | function == "set" = function ++ (if a then "i" else "r")
    | function `elem` ["eq", "gt"] = function ++ (if a then "i" else "r") ++ (if b then "i" else "r")
    | otherwise = function ++ (if b then "i" else "r")
    where function = detector f