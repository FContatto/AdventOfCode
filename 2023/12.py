def calc_combinations_ques_marks(ques_marks_len, damaged_nbs, cache, nbs_start_idx=0):
     if ques_marks_len == 0:
         return int(nbs_start_idx >= len(damaged_nbs))
     if ques_marks_len < 0:
         return 0
     if nbs_start_idx >= len(damaged_nbs):
         return 1
     if nbs_start_idx == len(damaged_nbs) - 1:
         return max(0, ques_marks_len - damaged_nbs[nbs_start_idx] + 1)
     if damaged_nbs[nbs_start_idx] > ques_marks_len:
         return 0
     ques_marks_len -= sum(damaged_nbs[nbs_start_idx:]) - (len(damaged_nbs) - nbs_start_idx)
     damaged_nbs = [1] * len(damaged_nbs)
     comb_key = ('?'*ques_marks_len, tuple([1] *(len(damaged_nbs)-nbs_start_idx)))
     if comb_key in cache:
         return cache[comb_key]
 
     ret = 0
     for prev_qs in range(ques_marks_len + 1):
         if ques_marks_len - damaged_nbs[nbs_start_idx] - prev_qs - 1 < 0:
             cache[comb_key] = ret
             return ret
         ret += calc_combinations_ques_marks(ques_marks_len - damaged_nbs[nbs_start_idx] - prev_qs - 1, damaged_nbs,
                                             cache, nbs_start_idx + 1)
     cache[comb_key] = ret
     return ret
 
 def calc_combinations_in_chunk(chunk, nbs, cache, chunk_start_idx=0, nbs_start_idx=0):
     comb_key = (chunk[chunk_start_idx:], tuple(nbs)[nbs_start_idx:])
     if comb_key in cache:
         return cache[comb_key]
     if nbs_start_idx >= len(nbs):
         return int('#' not in chunk[chunk_start_idx:])
     if chunk_start_idx >= len(chunk):
         return int(nbs_start_idx >= len(nbs))
     if '#' not in chunk[chunk_start_idx:]:
         return calc_combinations_ques_marks(len(chunk) - chunk_start_idx, nbs, cache, nbs_start_idx)
     if '?' not in chunk[chunk_start_idx:]:
         return int((nbs_start_idx == len(nbs) - 1) and (nbs[nbs_start_idx] == len(chunk) - chunk_start_idx))
     defect_chunks = [len(c) for c in chunk[chunk_start_idx:].split('?') if c != '']
 
     question_chunks = [len(c) for c in chunk[chunk_start_idx:].split('#') if c != '']
 
     if chunk[chunk_start_idx] == '#':
         if defect_chunks[0] == nbs[nbs_start_idx]:
             ret_comb = calc_combinations_in_chunk(chunk, nbs, cache,
                                                   chunk_start_idx + nbs[nbs_start_idx] + 1, nbs_start_idx + 1)
 
             cache[comb_key] = ret_comb
             return ret_comb
         if defect_chunks[0] > nbs[nbs_start_idx]:
             cache[comb_key] = 0
             return 0
 
         if defect_chunks[0] + question_chunks[0] < nbs[nbs_start_idx]:
             nbs[nbs_start_idx] -= defect_chunks[0] + question_chunks[0]
             ret_comb = calc_combinations_in_chunk(chunk, nbs, cache,
                                                   chunk_start_idx + defect_chunks[0] + question_chunks[0],
                                                   nbs_start_idx)
             nbs[nbs_start_idx] += defect_chunks[0] + question_chunks[0]
             cache[comb_key] = ret_comb
             return ret_comb
         if defect_chunks[0] + question_chunks[0] == nbs[nbs_start_idx]:
             ret_comb = int((nbs_start_idx == len(nbs) - 1) and len(defect_chunks) == 1)
             cache[comb_key] = ret_comb
             return ret_comb
         ret_comb = calc_combinations_in_chunk(chunk, nbs, cache, chunk_start_idx + nbs[nbs_start_idx] + 1,
                                               nbs_start_idx + 1)
         cache[comb_key] = ret_comb
         return ret_comb
 
     comb_sum = 0
     for i in range(nbs[nbs_start_idx] - 1, question_chunks[0] - 1):
         comb_sum += calc_combinations_in_chunk(chunk, nbs, cache, chunk_start_idx + i + 2, nbs_start_idx + 1)
 
     if defect_chunks[0] > nbs[nbs_start_idx]:
         cache[comb_key] = comb_sum
         return comb_sum
 
     if defect_chunks[0] == nbs[nbs_start_idx]:
         comb_sum += calc_combinations_in_chunk(chunk, nbs, cache,
                                                chunk_start_idx + question_chunks[0] + defect_chunks[0] + 1,
                                                nbs_start_idx + 1)
         cache[comb_key] = comb_sum
         return comb_sum
 
     for pre_defs_len in range(nbs[nbs_start_idx] - defect_chunks[0] + 1):
         if pre_defs_len > question_chunks[0]:
             break
         nbs[nbs_start_idx] -= pre_defs_len
         comb_sum += calc_combinations_in_chunk(chunk, nbs, cache,
                                                chunk_start_idx + question_chunks[0], nbs_start_idx)
         nbs[nbs_start_idx] += pre_defs_len
     cache[comb_key] = comb_sum
     return comb_sum
 
 
 def calc_sum_combinations(template_chunks, nbs, cache, start_idx=0):
 
     if start_idx >= len(template_chunks):
         return int(len(nbs) == 0)
     if len(nbs) == 0:
         return int(all(('#' not in c) for c in template_chunks[start_idx:]))
 
     if start_idx == len(template_chunks) - 1:
         return calc_combinations_in_chunk(template_chunks[start_idx], nbs, cache)
 
     combs_sum = 0
     for i in range(len(nbs) + 1):
         if i > len(template_chunks[start_idx]):
             break
         combs_first_chunk = calc_combinations_in_chunk(template_chunks[start_idx], nbs[:i],
                                                        cache)
         if combs_first_chunk == 0:
             continue
         combs_sum += combs_first_chunk * calc_sum_combinations(template_chunks, nbs[i:], cache, start_idx + 1)
     return combs_sum
 
 
 def calc_combinations(word):
     template_str, nbs_str = word.split()
     mult = 5
     template_str = '?'.join([template_str] * mult)
     nbs_str = ','.join([nbs_str] * mult)
     print(template_str + ' ' + nbs_str)
     nbs = [int(i) for i in nbs_str.split(',')]
     template_chunks = (' '.join(template_str.split('.'))).split()
     cache = dict()
     return calc_sum_combinations(template_chunks, nbs, cache)
 
 
 def calc_total_combination_sum(words):
     total_sum = 0
     for i, w in enumerate(words):
         print(i)
         combs = calc_combinations(w)
         print('combinations: ' + str(combs))
         total_sum += combs
         print('cumulative sum: ' + str(total_sum))
     return total_sum
 
 print(calc_total_combination_sum(words))