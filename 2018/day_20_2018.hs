import System.IO
import Data.List
import qualified Data.Map as Map
import qualified Data.Set as Set

main = do
    inputFile <- openFile "2018/inputs/day_20_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputString = init $ tail contents
    let inputMap = generateMap inputString
    print $ bfs inputMap
    print $ bfs2 inputMap
    putStrLn "done!"

bfs = bfs' (Set.singleton (0, 0)) Set.empty 0
bfs' frontier visited timer givenMap
    | Set.null frontier = timer - 1
    | otherwise = bfs' newFrontier (Set.union frontier visited) (timer + 1) givenMap
    where newFrontier = Set.filter (`Set.notMember` visited) $ Set.unions $ Set.map (givenMap Map.!) frontier

bfs2 = bfs2' (Set.singleton (0, 0)) Set.empty 0 0
bfs2' frontier visited timer total givenMap
    | Set.null frontier = total
    | timer >= 1000 = bfs2' newFrontier (Set.union frontier visited) (timer + 1) (total + Set.size frontier) givenMap
    | otherwise = bfs2' newFrontier (Set.union frontier visited) (timer + 1) total givenMap
    where newFrontier = Set.filter (`Set.notMember` visited) $ Set.unions $ Set.map (givenMap Map.!) frontier

generateMap = generateMap' (0, 0) [] (Map.fromList [((0, 0), Set.empty)])

generateMap' _ _ rollingMap [] = rollingMap
generateMap' pointer referenceStack rollingMap (char:chars) = case char of
    '(' -> generateMap' pointer (pointer:referenceStack) rollingMap chars
    '|' -> generateMap' (head referenceStack) referenceStack rollingMap chars
    ')' -> generateMap' pointer (tail referenceStack) rollingMap chars
    _   -> generateMap' nextPosition referenceStack (addLink pointer nextPosition rollingMap) chars
    where nextPosition = addTup pointer $ getDirection char

addTup (x1, y1) (x2, y2) = (x1 + x2, y1 + y2)

getDirection char = case char of
    'N' -> (0, -1)
    'E' -> (1, 0)
    'S' -> (0, 1)
    'W' -> (-1, 0)

addLink positionA positionB rollingMap
    | exists = Map.adjust (Set.insert positionA) positionB nextMap'
    | otherwise = Map.insert positionB (Set.singleton positionA) nextMap'
    where exists = Map.member positionB rollingMap
          nextMap' = Map.adjust (Set.insert positionB) positionA rollingMap
