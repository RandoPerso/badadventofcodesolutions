import System.IO
import Data.List (foldl')
import qualified Data.Map as Map
import Data.Maybe
import Debug.Trace

main = do
    inputFile <- openFile "2025/inputs/day_11_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = Map.fromList $ map parse $ lines contents
    print $ snd $ doSearch inputLines Map.empty "you"
    print $ snd $ doSearch2 inputLines Map.empty ("svr", False, False)
    putStrLn "done!"

parse x = (init $ head a, tail a)
    where a = words x

doSearch graph memory current
    | current == "out" = (memory, 1)
    | isJust memoed = (memory, fromJust memoed)
    | otherwise = (Map.insert current result newMem, result)
    where memoed = Map.lookup current memory
          (newMem, result) = foldl' (doStep graph) (memory, 0) (graph Map.! current)
    

doStep graph (memory, acc) next
    | next == "out" = (memory, 1)
    | isJust memoed = (memory, acc + fromJust memoed)
    | otherwise = (newMem, acc + result)
    where memoed = Map.lookup next memory
          (newMem, result) = doSearch graph memory next

getName (a,_,_) = a
validFlags (_,b,c) = b && c
getFlags (_,b,c) = (b,c)

doSearch2 graph memory current
    | getName current == "out" = if validFlags current then (memory, 1) else (memory, 0)
    | isJust memoed = (memory, fromJust memoed)
    | otherwise = (Map.insert current result newMem, result)
    where memoed = Map.lookup current memory
          (dac, fft) = getFlags current
          newDac = dac || getName current == "dac"
          newFft = fft || getName current == "fft"
          (newMem, result) = foldl' (doStep2 graph) (memory, 0) (map (,newDac,newFft) (graph Map.! getName current))
    

doStep2 graph (memory, acc) next
    | getName next == "out" = if validFlags next then (memory, 1) else (memory, 0)
    | isJust memoed = (memory, acc + fromJust memoed)
    | otherwise = (newMem, acc + result)
    where memoed = Map.lookup next memory
          (newMem, result) = doSearch2 graph memory next
