import System.IO
import qualified Data.Set as Set
import qualified Data.Map as Map
import Data.List (elemIndex)
import Data.Maybe

main = do
    inputFile <- openFile "2025/inputs/day_7_2025.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    print $ doIt 0 (Set.singleton $ fromJust ('S' `elemIndex` head inputLines)) inputLines
    print $ doIt2 (Map.singleton (fromJust ('S' `elemIndex` head inputLines)) 1) inputLines
    putStrLn "done!"

doIt total state (x:xs) = doIt newTotal newState xs
    where newState = setFlat $ Set.map (\y -> if x !! y == '^' then Set.fromList [y-1, y+1] else Set.singleton y) state
          newTotal = total + Set.size (Set.filter (\y -> x !! y == '^') state)
doIt total _ [] = total

setFlat = Set.unions

doIt2 state (x:xs) = doIt2 newState xs
    where newState = dictFlat $ Map.mapWithKey (\y i -> if x !! y == '^' then Map.fromList [(y-1, i), (y+1, i)] else Map.singleton y i) state
doIt2 state [] = sum $ Map.elems state

dictFlat = Map.unionsWith (+)
