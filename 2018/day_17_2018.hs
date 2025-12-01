import System.IO
import Data.List
import qualified Data.Set as Set

main = do
    inputFile <- openFile "2018/inputs/day_17_2018_ex.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    -- let wallsFunctions = map parse inputLines
    let walls = Set.fromList $ concatMap parse inputLines
    let yValues = concatMap parse2 inputLines
    let minY = minimum yValues
    let maxY = maximum yValues
    putStrLn "done!"

addWater maxY walls visited frontier location@(x, y) = evaluateWater maxY walls (unionWithList visited locations) nextFront
    where locations = reverse $ takeWhile (\test@(x1, y1) -> not (test `Set.member` walls && y1 > maxY)) ([(x, b) | b <- [y + 1..]])
          fell = snd (head locations) + 1 == maxY
          nextFront = if fell then frontier else locations ++ frontier

evaluateWater _ _ visited [] = 0
evaluateWater maxY walls visited (water@(x, y):waters) = 0
    where valid location = not $ location `Set.member` walls || downOne location `Set.member` walls
          rightLocations = takeWhile valid ([(a, y) | a <- [x..]])
          rightBrokenLocation = tupAdd (1, 0) $ last rightLocations
          leftLocations = takeWhile valid ([(a, y) | a <- [x-1,x-2..]])
          leftBrokenLocation = tupAdd (-1, 0) $ last leftLocations
          newVisited = Set.union visited $ unionLists rightLocations leftLocations

downOne (x, y) = (x, y + 1)

tupAdd (x1, y1) (x2, y2) = (x1 + x2, y1 + y2)

unionWithList :: Set.Set (Integer, Integer) -> [(Integer, Integer)] -> Set.Set (Integer, Integer)
unionWithList = flip $ Set.union . Set.fromList

unionLists x y = Set.union (Set.fromList x) (Set.fromList y)

{-
parse x = (\(a, b) -> a == leftValue && b >= rightValue1 && b <= rightValue2) . (if leftVariable == 'y' then swap else id)
    where (left, right) = break (== ' ') x
          leftVariable = head left
          rightVariable = head right
          leftValue = read $ init $ drop 2 left :: Int
          [rightValue1, rightValue2] = map read $ wordsBy '.' $ drop 3 right :: [Int]
-}

parse x = [(if leftVariable == 'y' then swap else id) (leftValue, b) |
             b <- [rightValue1 .. rightValue2]]
    where (left, right) = break (== ' ') x
          leftVariable = head left
          leftValue = read $ init $ drop 2 left :: Int
          [rightValue1, rightValue2] = map read $ wordsBy '.' $ drop 3 right :: [Int]

parse2 x = if leftVariable == 'y' then [leftValue] else [rightValue1, rightValue2]
    where (left, right) = break (== ' ') x
          leftVariable = head left
          leftValue = read $ init $ drop 2 left :: Int
          [rightValue1, rightValue2] = map read $ wordsBy '.' $ drop 3 right :: [Int]

wordsBy separator s =  case dropWhile (== separator) s of
                                "" -> []
                                s' -> w : wordsBy separator s''
                                        where (w, s'') =
                                                break (== separator) s'

-- i am very aware that this is in Data.Tuple
swap (a, b) = (b, a)