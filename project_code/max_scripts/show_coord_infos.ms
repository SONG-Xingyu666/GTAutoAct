obj = getNodeByName "SKEL_Spine3"

animate on

(

at time 0(
    
    format "\n"
    
    -- Informations of parent object
    TM_parent = obj.parent.transform
    format "Transform matrix parent: [%]\n" TM_parent
    TM_parent_I = Inverse(TM_parent)
    format "Transform matrix parent inverse: [%]\n" TM_parent_I

    -- Informations of child object
    coord_child_world = obj.pos
    format "Child obj coord in world coordsys: [%]\n" coord_child_world
    coord_child_parent = coordsys parent obj.pos
    format "Child obj coord in parent coordsys: [%]\n" coord_child_parent

    -- Calculate the local coord of child obj
    -- Coordinate of child node in parent system 
    --      = coordinate of child node in world system * inverse transform matrix of parent node  
    coord_child_local = coord_child_world * TM_parent_I
    format "Child obj coord in local coordsys: [%]\n" coord_child_local

    format "\n"


)
)
