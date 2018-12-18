package main

import (
	"fmt"
	"github.com/kierachell/practice/data"
)

func main() {
	fmt.Printf("Main function")
}

func twoSum(arr []int, target int) []int {
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

func addTwoNumbers(l1 *data.ListNode, l2 *data.ListNode) *data.ListNode {
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

func lengthOfLongestSubstring(s string) int {
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

func hashRabinKarp(text string, pattern string) int {
	textBytes := []byte(text)
	patternBytes := []byte(pattern)
	prime := 32452867
	alphabet := 256
	var j int
	N := len(text)
	M := len(pattern)
	patHash := 0
	textHash := 0
	h := 1
	for i := 0; i < M-1; i++ {
		h = (h * alphabet) % prime
	}

	for i := 0; i < M; i++ {
		patHash = (alphabet*patHash + int(patternBytes[i])) % prime
		textHash = (alphabet*textHash + int(textBytes[i])) % prime
	}

	for i := 0; i <= N; i++ {
		if patHash == textHash {
			for j = 0; j < M; j++ {
				if textBytes[i+j] != patternBytes[j] {
					break
				}
			}

			if j == M {
				return i
			}
		}

		if i < N-M {
			textHash = (alphabet*(textHash-int(textBytes[i])*h) + int(textBytes[i+M])) % prime
			if textHash < 0 {
				textHash = textHash + prime
			}
		}
	}
	return -1
}
