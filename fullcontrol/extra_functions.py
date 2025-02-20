from fullcontrol.common import Point
from copy import deepcopy


def points_only(steps: list, track_xyz: bool = True) -> list:
    ''' convert steps of Points and control to only Points. return new list. 
    If track_xyz=False, Points are returned as they are defined, including attributes with value=None
    If track_xyz=True, the returned list contains a tracked list of points with all of xyz
    defined: when some of xyz are not defined, they are calculated from previous step. The first point 
    in the returned list will be the point for which all xyz were defined/tracked. 
    '''
    new_steps = []
    # remove all data that isn't a Point
    for i in range(len(steps)):
        if type(steps[i]).__name__ == 'Point':
            new_steps.append(steps[i])
    if track_xyz:
        for i in range(len(new_steps)-1):
            # fill in any None attributes for the next point with the most recent previous value:
            next_point = deepcopy(new_steps[i])
            # update values that are not None
            next_point.update_from(new_steps[i+1])
            new_steps[i+1] = next_point
        # delete initial elements prior to all of x y and z have values != None:
        loop = True
        while loop:
            if new_steps[0].x == None or new_steps[0].y == None or new_steps[0].z == None:
                del new_steps[0]
            else:
                loop = False
    return new_steps


def flatten(steps: list) -> list:
    'takes a list in which some elements are lists in (second dimension). returns a flattenned 1D list'
    # alternative: https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists
    # xss = steplist
    # return [x for xs in xss for x in xs]
    count = 0
    for i in range(len(steps)):
        if type(steps[i+count]) == list:
            for j in range(len(steps[i+count])):
                # insert each element as a new element in the overall list after the current element
                steps.insert(i+1+count+j, steps[i+count][j])
            # delete the list element that is now flattened
            del steps[i+count]
            count += j
    return steps


def linspace(start: float, end: float, number_of_points: int) -> list:
    'generate evenly spaced floats from start to end. returns a list of number_of_points floats including start and end'
    return [start + float(x)/(number_of_points-1)*(end-start) for x in range(number_of_points)]


def check(steps: list):
    'check a list of steps and report what type of classes are included and whether the list is 2D. FullControl requires it to be 1D for processing'
    # potential things to add to this function: check the first point has all of X Y Z defined
    types = set()
    warning = ""
    if type(steps).__name__ == 'list':
        for i in range(len(steps)):
            types.add(type(steps[i]).__name__)
            if "list" in types:
                warning = "  warning - the list of steps must be a 1D list of fullcontrol class instances, it currently includes a 'list'\n  use fc.flatten() to convert it to 1D or check for accidental use of append() instead of extend()\n"
        print("check results:\n" + warning + "  step types: " + str(types))
    else:
        warning = "  warning - the design must be a 1D list of fullcontrol class instances, it currently a single object, not a list"
        print("check results:\n" + warning)


def first_point(steps: list, fully_defined: bool = True) -> Point:
    'return first Point in list. if the parameter fully_defined is true, return first Point with all x,y,z != None'
    if type(steps).__name__ == 'list':
        for i in range(len(steps)):
            if type(steps[i]).__name__ == 'Point':
                if fully_defined:
                    if steps[i].x != None and steps[i].y != None and steps[i].z != None:
                        return steps[i]
                else:
                    return steps[i]
    if fully_defined:
        raise Exception(f'No point found in steps with all of x y z defined')
    if not fully_defined:
        raise Exception(f'No point found in steps')


def export_design(steps: list, filename: str):
    'export design (list of steps) to filename.json'
    import json
    with open(filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(steps, f, ensure_ascii=False, indent=4, default=lambda x: {'type': type(x).__name__, 'data': x.__dict__})


def import_design(fc_module_handle, filename: str):
    'import a previously exported design (list of steps). fc_module_handle is the fc module that was imported to create the design originally (typically fc in documentation)'
    import json
    with open(filename + '.json') as f:
        data = json.load(f)
    steps = []
    for step in data:
        class_ = getattr(fc_module_handle, step['type'])
        step = class_.parse_obj(step['data'])
        steps.append(step)
    return steps
