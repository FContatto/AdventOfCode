words2 = '''px{a<2006:qkq,m>2090:A,rfg}
 pv{a>1716:R,A}
 lnx{m>1548:A,A}
 rfg{s<537:gd,x>2440:R,A}
 qs{s>3448:A,lnx}
 qkq{x<1416:A,crn}
 crn{x>2662:A,R}
 in{s<1351:px,qqz}
 qqz{s>2770:qs,m<1801:hdj,R}
 gd{a>3333:R,R}
 hdj{m>838:A,pv}
 
 {x=787,m=2655,a=1222,s=2876}
 {x=1679,m=44,a=2067,s=496}
 {x=2036,m=264,a=79,s=2244}
 {x=2461,m=1339,a=466,s=291}
 {x=2127,m=1623,a=2188,s=1013}'''
 
 class Part:
     def __init__(self, part_str):
         part_features_str = part_str[1:-1].split(',')
         part_features_str = [p.split('=') for p in part_features_str]
         self.features = {p[0]: int(p[1]) for p in part_features_str}
 
     def sum(self):
         return sum(self.features.values())
 
 class Condition:
     def __init__(self, condition_str):
         self.condition = None
         self.destination = condition_str
         if ':' in condition_str:
             self.condition, self.destination = condition_str.split(':')
 
     def apply(self, part):
         if self.condition is None:
             return self.destination
         if '>' in self.condition:
             category_cond, rating_cond = self.condition.split('>')
             rating_cond = int(rating_cond)
             if part.features[category_cond] > rating_cond:
                 return self.destination
         elif '<' in self.condition:
             category_cond, rating_cond = self.condition.split('<')
             rating_cond = int(rating_cond)
             if part.features[category_cond] < rating_cond:
                 return self.destination
         return False
 
 class Workflow:
     def __init__(self, workflow_str):
         condition_start_idx = workflow_str.index('{')
         self.name = workflow_str[:condition_start_idx]
         self.conditions = [Condition(c) for c in workflow_str[condition_start_idx+1:-1].split(',')]
 
     def apply(self, part):
         for c in self.conditions:
             destination = c.apply(part)
             if not destination:
                 continue
             return destination
 
 
 
 def calc_accepted_ratings(words):
     workflows = dict()
     parts = []
     is_workflow = True
     for w in words.split('\n'):
         if w == '':
             is_workflow = False
         elif is_workflow:
             w = Workflow(w)
             workflows[w.name] = w
         else:
             parts.append(Part(w))
     total_rating = 0
     for part in parts:
         workflow_name = 'in'
         while True:
             workflow = workflows[workflow_name]
             workflow_name = workflow.apply(part)
             if workflow_name in ['A', 'R']:
                 if workflow_name == 'A':
                     total_rating += part.sum()
                 break
 
     return total_rating
 
 def calc_nb_of_possible_ratings_from_bounds(bounds):
     nb_possibilities = 1
     for x,y in bounds.values():
         if y<x:
             return 0
         nb_possibilities *= y-x + 1
     return nb_possibilities
 
 def bounds_that_satisfy_condition(bounds, condition):
     if condition is None:
         return bounds
     new_bounds = None
     if '>' in condition:
         category_cond, rating_cond = condition.split('>')
         rating_cond = int(rating_cond)
         lower, upper = bounds[category_cond]
         if lower > rating_cond:
             return bounds
         if upper < rating_cond:
             return None
         new_bounds = {k: v for k,v in bounds.items()}
         new_bounds[category_cond] = (rating_cond+1, upper)
     elif '<' in condition:
         category_cond, rating_cond = condition.split('<')
         rating_cond = int(rating_cond)
         lower, upper = bounds[category_cond]
         if lower > rating_cond:
             return None
         if upper < rating_cond:
             return bounds
         new_bounds = {k: v for k, v in bounds.items()}
         new_bounds[category_cond] = (lower, rating_cond - 1)
     return new_bounds
 
 
 
 def bounds_that_not_satisfy_condition(bounds, condition):
     if condition is None:
         return None
     new_bounds = None
     if '>' in condition:
         category_cond, rating_cond = condition.split('>')
         rating_cond = int(rating_cond)
         lower, upper = bounds[category_cond]
         if lower > rating_cond:
             return None
         if upper < rating_cond:
             return bounds
         new_bounds = {k: v for k, v in bounds.items()}
         new_bounds[category_cond] = (lower, rating_cond)
     elif '<' in condition:
         category_cond, rating_cond = condition.split('<')
         rating_cond = int(rating_cond)
         lower, upper = bounds[category_cond]
         if lower > rating_cond:
             return bounds
         if upper < rating_cond:
             return None
         new_bounds = {k: v for k, v in bounds.items()}
         new_bounds[category_cond] = (rating_cond, upper)
     return new_bounds
 
 def calc_nb_possible_ratings_from_workflows(workflows, init_wf_name='in', bounds=None):
     if bounds is None:
         bounds = {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
     if init_wf_name == 'A':
         return calc_nb_of_possible_ratings_from_bounds(bounds)
     if init_wf_name == 'R':
         return 0
 
     workflow = workflows[init_wf_name]
     nb_ratings = 0
     for c in workflow.conditions:
         new_bounds = bounds_that_satisfy_condition(bounds, c.condition)
         if new_bounds is not None:
             nb_ratings += calc_nb_possible_ratings_from_workflows(workflows, c.destination, new_bounds)
         new_bounds = bounds_that_not_satisfy_condition(bounds, c.condition)
         if new_bounds is None:
             return nb_ratings
         bounds = new_bounds
     return nb_ratings
 
 def calc_nb_possible_ratings(words):
     workflows = dict()
     for w in words.split('\n'):
         if w == '':
             break
         w = Workflow(w)
         workflows[w.name] = w
 
     return calc_nb_possible_ratings_from_workflows(workflows)
 
 
 print(calc_nb_possible_ratings(words))