import System.IO
import qualified Data.Map as Map
import Data.List

main = do
    inputFile <- openFile "2018/inputs/day_13_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    let inputMap = foldrEnumerated parse Map.empty inputLines
    let cartsMap = foldrEnumerated parse2 Map.empty inputLines
    print $ untilCollision inputMap cartsMap
    print $ untilLonely inputMap cartsMap
    putStrLn "done!"

foldrEnumerated f accumulator xs = foldr (\(y, line) output -> foldr (f y) output (zip [0..] line)) accumulator (zip [0..] xs)

parse y (x, char) outputMap
    | char == ' ' = outputMap
    | char `elem` "|-^>v<"= Map.insert (x, y) 0 outputMap
    | char == '+' = Map.insert (x, y) 1 outputMap
    | char == '\\' = Map.insert (x, y) 2 outputMap
    | char == '/' = Map.insert (x, y) 3 outputMap

parse2 y (x, char) outputMap
    | char `elem` " |-+\\/" = outputMap
    | char == '^' = Map.insert (x, y) (0, -1, 0) outputMap
    | char == '>' = Map.insert (x, y) (1, 0, 0) outputMap
    | char == 'v' = Map.insert (x, y) (0, 1, 0) outputMap
    | char == '<' = Map.insert (x, y) (-1, 0, 0) outputMap

tupAdd' (x1, y1) (x2, y2, _) = (x1 + x2, y1 + y2)

tupRotCW (x, y) = (-y, x)
tupRotWS (x, y) = (y, -x)

repack (a, b) c = (a, b, c)

intersectRotate (dx, dy, intersectDir)
    | intersectDir == 0 = repack (tupRotWS (dx, dy)) 1
    | intersectDir == 1 = (dx, dy, 2)
    | otherwise = repack (tupRotCW (dx, dy)) 0

getNextDir char dir@(dx, dy, intersectDir)
    | char == 0 = dir
    | char == 1 = intersectRotate dir
    | char == 2 =
        if dy == 0 then
            repack (tupRotCW (dx, dy)) intersectDir
        else
            repack (tupRotWS (dx, dy)) intersectDir
    | otherwise =
        if dy == 0 then 
            repack (tupRotWS (dx, dy)) intersectDir
        else
            repack (tupRotCW (dx, dy)) intersectDir

untilCollision inputMap cartsMap
    | Map.member (-1, -1) nextCarts = nextCarts Map.! (-1, -1)
    | otherwise = untilCollision inputMap nextCarts
    where cartOrder = sortBy getOrder $ Map.keys cartsMap
          nextCarts = foldl (addMovedCart inputMap) cartsMap cartOrder

getOrder (x1, y1) (x2, y2)
    | y1 /= y2 = compare y1 y2
    | otherwise = compare x1 x2

addMovedCart inputMap outputMap cart
    | Map.member (-1, -1) outputMap = outputMap
    | Map.member nextCart outputMap = Map.insert (-1, -1) (repack nextCart 0) outputMap
    | otherwise = Map.insert nextCart nextDir $ Map.delete cart outputMap
    where nextDir = getNextDir (inputMap Map.! cart) (outputMap Map.! cart)
          nextCart = tupAdd' cart nextDir

untilLonely inputMap cartsMap
    | Map.size cartsMap == 1 = head $ Map.keys cartsMap
    | otherwise = untilLonely inputMap nextCarts
    where cartOrder = sortBy getOrder $ Map.keys cartsMap
          nextCarts = foldl (addMovedCart' inputMap) cartsMap cartOrder

addMovedCart' inputMap outputMap cart
    | not $ Map.member cart outputMap = outputMap
    | Map.member nextCart outputMap = Map.delete nextCart $ Map.delete cart outputMap
    | otherwise = Map.insert nextCart nextDir $ Map.delete cart outputMap
    where nextDir = getNextDir (inputMap Map.! cart) (outputMap Map.! cart)
          nextCart = tupAdd' cart nextDir
