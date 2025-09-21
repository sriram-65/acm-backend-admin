def Validate_all(title , cap , head1 , head2 , head3 , des1 , des2 , des3):
    res1 = Validate_title_caption_headings(title  , cap , head1 , head2 , head3)
    res2 = Validate_des(des1 , des2 , des3)
    
    if(res1!='passed'):
        return res1
    
    if(res2!='passed'):
        return res2
    

    return True


def Validate_title_caption_headings(title , cap , *head):
    if not title:
        return 'Pls Provide the Title'
    
    if not cap:
        return 'Pls Provide the Caption'
    
    if(len(head)<3):
        return 'Pls Provide All The Headings'
    
    return 'passed'



def Validate_des(*des):
    if len(des)<3:
        return 'pls Provide All the Descriptions'
    
    for i in des:
        if(len(i)>100):
            return 'Too long Description pls Reduce it'
    
    return 'passed'