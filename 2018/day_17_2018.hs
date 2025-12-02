import System.IO
import Data.List
import qualified Data.Set as Set
import Debug.Trace

main = do
    inputFile <- openFile "2018/inputs/day_17_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    -- let wallsFunctions = map parse inputLines
    let walls = Set.fromList $ concatMap parse inputLines
    let yValues = concatMap parse2 inputLines
    let minY = minimum yValues
    let maxY = maximum yValues
    putStrLn "done!"

parse x = [(if leftVariable == 'y' then swap else id) (leftValue, b) |
             b <- [rightValue1 .. rightValue2]]
    where (left, right) = break (== ' ') x
          leftVariable = head left
          leftValue = read $ init $ drop 2 left :: Integer
          [rightValue1, rightValue2] = map read $ wordsBy '.' $ drop 3 right :: [Integer]

parse2 x = if leftVariable == 'y' then [leftValue] else [rightValue1, rightValue2]
    where (left, right) = break (== ' ') x
          leftVariable = head left
          leftValue = read $ init $ drop 2 left :: Integer
          [rightValue1, rightValue2] = map read $ wordsBy '.' $ drop 3 right :: [Integer]

wordsBy separator s =  case dropWhile (== separator) s of
                                "" -> []
                                s' -> w : wordsBy separator s''
                                        where (w, s'') =
                                                break (== separator) s'

visualize (minX, maxX, minY, maxY) locations = unlines [[if Set.member (x, y) locations then '#' else '.' | x <- [minX..maxX]] | y <- [minY..maxY]]

-- i am very aware that this is in Data.Tuple
swap (a, b) = (b, a)

{-
main = do
    inputFile <- openFile "2018/inputs/day_17_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputLines = lines contents
    -- let wallsFunctions = map parse inputLines
    let walls = Set.fromList $ concatMap parse inputLines
    let yValues = concatMap parse2 inputLines
    let minY = minimum yValues
    let maxY = maximum yValues
    let beginning = fst $ addWater maxY walls (500, 0)
    -- writeFile "2018/temp.txt" $ visualize (0, 2000, 0, maxY) walls
    let outputSet = Set.filter ((>= minY) . snd) $ Set.difference (snd $ evaluateWater maxY walls (Set.fromList beginning) beginning) walls
    print $ Set.size outputSet
    -- putStrLn $ visualize (494,507,0,13) outputSet
    -- writeFile "2018/temp.txt" $ visualize (200, 600, 0, maxY) outputSet
    putStrLn "done!"

addWater maxY walls (x, y) = (locations, fell)
    where locations = reverse $ takeWhile (\test@(x1, y1) -> not (test `Set.member` walls || y1 > maxY)) ([(x, b) | b <- [y..]])
          fell = not (null locations) && (snd (head locations) + 2 == maxY)

evaluateWater _ walls visited [] = (walls, visited)
evaluateWater maxY walls visited (water@(x, y):waters)
    | not canMove = evaluateWater maxY walls visited waters
    | otherwise = evaluateWater maxY newWalls newVisited waters
    where valid location = not (location `Set.member` walls) && (downOne location `Set.member` walls)
          canMove = (tupAdd (0, 1) water `Set.member` walls) && not (water `Set.member` walls)
          rightLocations = takeWhile valid ([(a, y) | a <- [x..]])
          rightBrokenLocation = tupAdd (1, 0) $ last rightLocations
          leftLocations = takeWhile valid ([(a, y) | a <- [x-1,x-2..]])
          leftBrokenLocation = tupAdd (-1, 0) $ if null leftLocations then water else last leftLocations
          rightHasWall = rightBrokenLocation `Set.member` walls
          leftHasWall = leftBrokenLocation `Set.member` walls
          (leftLocations2, leftFell) = addWater maxY walls leftBrokenLocation
          (rightLocations2, rightFell) = addWater maxY walls rightBrokenLocation
          (leftWalls, leftVisited) = evaluateWater maxY walls (Set.fromList leftLocations2) leftLocations2
          (rightWalls, rightVisited) = evaluateWater maxY walls (Set.fromList rightLocations2) rightLocations2
          newWalls = Set.union walls $ case (leftHasWall, rightHasWall) of
            (True, True) -> unionLists leftLocations rightLocations
            (True, _)    -> unionWithList rightWalls leftLocations
            (_, True)    -> unionWithList leftWalls rightLocations
            (_, _)       -> Set.union leftWalls rightWalls
          newVisited' = Set.union walls $ case (leftHasWall, rightHasWall) of
            (False, False) -> Set.union leftVisited rightVisited
            (False, _)    -> leftVisited
            (_, False)    -> rightVisited
            (_, _)       -> Set.empty
          newVisited = Set.union visited $ Set.union newVisited' $ unionManyLists [leftLocations, rightLocations]
          -- _ = if canMove && Set.size newVisited > Set.size visited then traceShowId $ Set.size visited else 0

downOne (x, y) = (x, y + 1)

tupAdd (x1, y1) (x2, y2) = (x1 + x2, y1 + y2)

unionWithList :: Set.Set (Integer, Integer) -> [(Integer, Integer)] -> Set.Set (Integer, Integer)
unionWithList = flip $ Set.union . Set.fromList

unionLists :: [(Integer, Integer)] -> [(Integer, Integer)] -> Set.Set (Integer, Integer)
unionLists x y = Set.union (Set.fromList x) (Set.fromList y)

unionManyLists :: [[(Integer, Integer)]] -> Set.Set (Integer, Integer)
unionManyLists = foldr (Set.union . Set.fromList) Set.empty

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
          leftValue = read $ init $ drop 2 left :: Integer
          [rightValue1, rightValue2] = map read $ wordsBy '.' $ drop 3 right :: [Integer]

parse2 x = if leftVariable == 'y' then [leftValue] else [rightValue1, rightValue2]
    where (left, right) = break (== ' ') x
          leftVariable = head left
          leftValue = read $ init $ drop 2 left :: Integer
          [rightValue1, rightValue2] = map read $ wordsBy '.' $ drop 3 right :: [Integer]

wordsBy separator s =  case dropWhile (== separator) s of
                                "" -> []
                                s' -> w : wordsBy separator s''
                                        where (w, s'') =
                                                break (== separator) s'

visualize (minX, maxX, minY, maxY) locations = unlines [[if Set.member (x, y) locations then '#' else '.' | x <- [minX..maxX]] | y <- [minY..maxY]]

-- i am very aware that this is in Data.Tuple
swap (a, b) = (b, a)
-}