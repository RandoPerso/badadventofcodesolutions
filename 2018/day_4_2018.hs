import System.IO
import Data.List
import Data.Maybe
import qualified Data.Map as Map

main = do
    inputFile <- openFile "2018/inputs/day_4_2018.txt" ReadMode
    contents <- hGetContents inputFile
    let inputList = sortBy (\a b -> compare (getTime a) (getTime b)) (lines contents)
    let sleepyMap = findSleepy inputList "#" 0 Map.empty
    let sleepyGuard = fst (findMaxKeyValue "#" 0 (Map.toList sleepyMap))
    let sleepyTimesList = makeSleepyTimes inputList sleepyGuard False 0 (replicate 60 0)
    let sleepiestTime = findMaxIndex sleepyTimesList :: Int
    print ((read $ drop 1 sleepyGuard :: Int) * sleepiestTime)
    let oftenSleepiest = findOftenSleepy "#" 0 0 inputList (Map.keys sleepyMap)
    print ((read $ drop 1 (fst oftenSleepiest) :: Int) * snd oftenSleepiest)
    putStrLn "done!"

getTime x = take 11 $ drop 6 x
getMinutes x = read (take 2 $ drop 15 x) :: Int

findSleepy [] currentGuard timeAsleep totalTimeMap = totalTimeMap
findSleepy (action:actions) currentGuard timeAsleep totalTimeMap
    | words action !! 2 == "Guard" = findSleepy actions (words action !! 3) timeAsleep totalTimeMap
    | words action !! 2 == "falls" = findSleepy actions currentGuard (getMinutes action) totalTimeMap
    | otherwise = if Map.member currentGuard totalTimeMap then
        findSleepy actions currentGuard timeAsleep (Map.update (\x -> Just $ x + (getMinutes action - timeAsleep)) currentGuard totalTimeMap)
      else
        findSleepy actions currentGuard timeAsleep (Map.insert currentGuard (getMinutes action - timeAsleep) totalTimeMap)


findMaxKeyValue maxKey maxValue [] = (maxKey, maxValue)
findMaxKeyValue maxKey maxValue (guard:guards)
    | snd guard > maxValue = uncurry findMaxKeyValue guard guards
    | otherwise = findMaxKeyValue maxKey maxValue guards

makeSleepyTimes :: [String] -> String -> Bool -> Int -> [Int] -> [Int]
makeSleepyTimes [] guard onShift timeAsleep sleepyTimesList = sleepyTimesList
makeSleepyTimes (action:actions) guard onShift timeAsleep sleepyTimesList
    | words action !! 2 == "Guard" = makeSleepyTimes actions guard (words action !! 3 == guard) timeAsleep sleepyTimesList
    | onShift && words action !! 2 == "falls" = makeSleepyTimes actions guard onShift (getMinutes action) sleepyTimesList
    | onShift = makeSleepyTimes actions guard onShift timeAsleep (mapIndex (\x y -> if y >= timeAsleep && y < getMinutes action then x + 1 else x) sleepyTimesList)
    | otherwise = makeSleepyTimes actions guard onShift timeAsleep sleepyTimesList

mapIndex f x = mapIndex' f x 0 []

mapIndex' f [] index running = running
mapIndex' f (item:list) index running = mapIndex' f list (index + 1) (running ++ [f item index])

findMaxIndex x = findMaxIndex' 0 0 x 0
findMaxIndex' maxIndex runningMax [] index = maxIndex
findMaxIndex' maxIndex runningMax (x:y) index = findMaxIndex' (if x > runningMax then index else maxIndex) (max x runningMax) y (index + 1)

findSleepiestMinute actions guard = findMaxIndex $ makeSleepyTimes actions guard False 0 (replicate 60 0)

findOftenSleepy guard sleepAmount sleepTime actions [] = (guard, sleepTime)
findOftenSleepy guard sleepAmount sleepTime actions (candidate:guards)
    | maximum (makeSleepyTimes actions candidate False 0 (replicate 60 0)) > sleepAmount = findOftenSleepy candidate (maximum (makeSleepyTimes actions candidate False 0 (replicate 60 0))) (findSleepiestMinute actions candidate) actions guards
    | otherwise = findOftenSleepy guard sleepAmount sleepTime actions guards
