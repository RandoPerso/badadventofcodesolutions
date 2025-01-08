import System.IO
import Data.List
import qualified Data.Map as Map
import Data.Maybe
import Data.Char

main = do
    inputFile <- openFile "2018/inputs/day_7_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let (dependencies, allows) = construct inputLines
    let order = presses dependencies allows
    putStrLn order
    let (charDependencies, charAllows) = (makeChar dependencies, makeChar allows)
    print $ working charDependencies charAllows
    putStrLn "done!"

safeAdd key element x
    | Map.member key x = Map.adjust (element :) key x
    | otherwise = Map.insert key [element] x

parse x = (separated !! 1, separated !! 7)
    where separated = words x

construct x = construct' x Map.empty Map.empty

construct' [] dependencies allows = sync (dependencies, allows)
construct' (x:xs) dependencies allows = construct' xs (safeAdd (snd instruction) (fst instruction) dependencies) (uncurry safeAdd instruction allows)
    where instruction = parse x

sync (dependencies, allows) = (foldr addBlank dependencies (Map.keys allows), foldr addBlank allows (Map.keys dependencies))

addBlank x y = if not $ Map.member x y then Map.insert x [] y else y

findNext dependencies allows
    | Map.null allows = ""
    | otherwise = minimum $ filter (\x -> null (fromJust $ Map.lookup x dependencies)) (Map.keys allows)

removeThisFrom value keys x = foldr (Map.adjust (delete value)) x keys

presses dependencies allows = presses' dependencies allows []

presses' dependencies allows output
    | Map.null allows = concat $ reverse output
    | otherwise = presses' (removeThisFrom next (fromJust $ Map.lookup next allows) dependencies) (Map.delete next allows) (next:output)
    where next = findNext dependencies allows

makeChar = Map.foldrWithKey (\k a b -> Map.insert (head k) (map head a) b) Map.empty

findAllNext dependencies allows excluded = filter (\x -> notElem x excluded && null (fromJust $ Map.lookup x dependencies)) (Map.keys allows)

working dependencies allows = assign dependencies allows (replicate 5 (' ', -1)) 0

getCharValue x = ord x - 4

assignGiven [] possible time = []
assignGiven workers [] time = workers
assignGiven (worker:workers) possible time
    | fst worker == ' ' = (head possible, time + getCharValue (head possible)) : assignGiven workers (tail possible) time
    | otherwise = worker : assignGiven workers possible time

assign dependencies allows workers time
    | Map.null allows = time
    | otherwise = finishUp dependencies allows (assignGiven workers nextUp time) (time + 1)
    where nextUp = sort $ findAllNext dependencies allows (map fst workers)

finishUp dependencies allows workers time = assign (foldr (\x y -> removeThisFrom x (fromJust $ Map.lookup x allows) y) dependencies finished) (foldr Map.delete allows finished) (map (\x -> if snd x == time then (' ', -1) else x) workers) time
    where finished = map fst $ filter (\x -> time == snd x) workers
