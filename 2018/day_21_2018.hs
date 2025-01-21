import System.IO
import Data.List
import Data.Bits
import qualified Data.Map as Map
import qualified Data.Set as Set
import Data.Maybe

main = do
    inputFile <- openFile "2018/inputs/day_21_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let rightVariableOperations = map (, [False], [False, True]) [(+), (*), (.&.), (.|.)] :: [(Int -> Int -> Int, [Bool], [Bool])]
    let dualVariableOperations = map (, [False, True], [False, True]) [(boolToInt .) . (>), (boolToInt .) . (==)]
    let allOperations' = (leftId, [False, True], [False]):rightVariableOperations ++ dualVariableOperations
    let allOperations = concatMap (\(operation, variableA, variableB) -> [(operation, x, y) | x <- variableA, y <- variableB, not $ x && y]) allOperations'
    let operationsMap = Map.fromList $ map (\operation -> (convert operation, operation)) allOperations
    let ipRegister = read [head inputLines !! 4] :: Int
    let instructionsMap = Map.fromList $ zip [0..] $ map (parse operationsMap) $ tail inputLines
    let importantLine = words $ inputLines !! (length inputLines - 3)
    let importantRegister = if importantLine !! 1 == "0" then read $ importantLine !! 2 else read $ importantLine !! 1 :: Int
    let correctValue = runUntil ipRegister instructionsMap (replicate 6 0) !! importantRegister
    print correctValue
    {-
    let correctValue2 = runAgain importantRegister Set.empty 0 ipRegister instructionsMap (replicate 6 0)
    print correctValue2
    -}
    {-
    let newValues = reverse $ runSomeOfIt importantRegister [] ipRegister instructionsMap (replicate 6 0)
    writeFile "temp.txt" $ unlines newValues
    -}
    {-
    let someIterations = iterate runOne (Set.empty, 0)
    print $ someIterations !! 3 
    -}
    putStrLn "WARNING: the following number is specific to my input."
    print $ runAllOfIt Set.empty 0
    putStrLn "done!"

-- WARNING, the function below is personalized. it will not work for you.
runAllOfIt visited previous
    | Set.member next4 visited = previous
    | otherwise = runAllOfIt (Set.insert next4 visited) next4
    where next3' = previous .|. 65536
          next4' = 12670166
          next4 = doAThing next3' next4'

{-
runOne (visited, previous) = (Set.insert next4 visited, next4)
    where next3' = previous .|. 65536
          next4' = 12670166
          next4 = doAThing next3' next4'
-}

doAThing current3 current4
    | current3 < 256 = next4
    | otherwise = doAThing next3 next4
    where next4 = kr24 $ kr24 (current4 + kr8 current3) * 65899
          next3 = shiftR current3 8

keepRightmostN x n = x .&. (2 ^ n - 1)

kr8 :: Int -> Int
kr8 = flip keepRightmostN 8
kr24 = flip keepRightmostN 24

{-
runSomeOfIt importantRegister visited ipRegister instructionsMap registers
    | (registers !! ipRegister) == (Map.size instructionsMap - 3) =
        if length visited == 100 then 
            visited
        else
            runSomeOfIt importantRegister (show (registers !! importantRegister) : visited) ipRegister instructionsMap (mutateList registers ipRegister (registers !! ipRegister + 2))
    | otherwise = runSomeOfIt importantRegister visited ipRegister instructionsMap nextState
    where nextInstruction = Map.lookup (registers !! ipRegister) instructionsMap
          nextState' = fromJust nextInstruction registers
          nextIP = (nextState' !! ipRegister) + 1
          nextState = mutateList nextState' ipRegister nextIP
-}

{-
runAgain importantRegister visited previous ipRegister instructionsMap registers
    | (registers !! ipRegister) == (Map.size instructionsMap - 3) =
        if Set.member (registers !! importantRegister) visited then
            previous
        else
            runAgain importantRegister (Set.insert (registers !! importantRegister) visited) (registers !! importantRegister) ipRegister instructionsMap (mutateList registers ipRegister (registers !! ipRegister + 2))
    | otherwise = runAgain importantRegister visited previous ipRegister instructionsMap nextState
    where nextInstruction = Map.lookup (registers !! ipRegister) instructionsMap
          nextState' = fromJust nextInstruction registers
          nextIP = (nextState' !! ipRegister) + 1
          nextState = mutateList nextState' ipRegister nextIP
-}

runUntil ipRegister instructionsMap registers
    | (registers !! ipRegister) == (Map.size instructionsMap - 3) = registers
    | otherwise = runUntil ipRegister instructionsMap nextState
    where nextInstruction = Map.lookup (registers !! ipRegister) instructionsMap
          nextState' = fromJust nextInstruction registers
          nextIP = (nextState' !! ipRegister) + 1
          nextState = mutateList nextState' ipRegister nextIP

doIt = doIt' Set.empty
doIt' previousStates ipRegister instructionsMap registers
    | isNothing nextInstruction = True
    | (ipRegister, registers) `Set.member` previousStates = False
    | otherwise = doIt' (Set.insert (ipRegister, registers) previousStates) ipRegister instructionsMap nextState
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