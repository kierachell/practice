package algorithms

import (
	"github.com/kierachell/practice/data"
)

func TwoSum(arr []int, target int) []int {
	indicies := make([]int, 2)
	complements := make(map[int]int)
	for idx, val := range arr {
		if compl, ok := complements[val]; ok {
			indicies[0] = idx
			indicies[1] = compl
			return indicies
		}
		complements[target-val] = idx
	}
	return indicies
}

func AddTwoNumbers(l1 *data.ListNode, l2 *data.ListNode) *data.ListNode {
	carry := 0
	sumNode := data.ListNode{
		Val: 0,
	}
	next := &sumNode
	for {
		next.Val += carry
		carry = 0
		if l2 != nil {
			next.Val += l2.Val
			l2 = l2.Next
		}
		if l1 != nil {
			next.Val += l1.Val
			l1 = l1.Next
		}
		if next.Val >= 10 {
			carry = 1
			next.Val = next.Val % 10
		}
		if l1 != nil || l2 != nil {
			next.Next = &data.ListNode{}
			next = next.Next
		} else {
			break
		}
	}
	if carry > 0 {
		next.Next = &data.ListNode{
			Val: carry,
		}
	}
	return &sumNode
}

func LengthOfLongestSubstring(s string) int {
	byteArray := []byte(s)
	maxLen := 0
OUTER:
	for outerIdx, _ := range byteArray {
		charSet := make(map[byte]bool)
		for innerIdx, char := range byteArray[outerIdx:] {
			if _, found := charSet[char]; found {
				if innerIdx > maxLen {
					maxLen = len(charSet)
				}
				continue OUTER
			}
			charSet[char] = true
		}
		if len(charSet) > maxLen {
			maxLen = len(charSet)
		}
	}
	return maxLen
}

func AnagramSearch(pattern string, text string) []int {
	var indecies []int
	pLen := len(pattern)
	tLen := len(text)
	countP := make(map[rune]int, pLen)
	countW := make(map[rune]int, pLen)
	for idx, char := range pattern {
		countP[char] += 1
		countW[[]rune(text)[idx]] += 1
	}

	compare := func(countP, countW map[rune]int) bool {
		for key, val := range countW {
			if countP[key] != val {
				return false
			}
		}
		return true
	}

	for idx := pLen; idx < tLen; idx++ {
		if compare(countP, countW) {
			indecies = append(indecies, idx-pLen)
		}
		countW[[]rune(text)[idx]] += 1
		countW[[]rune(text)[idx-pLen]] -= 1
	}
	return indecies
}
