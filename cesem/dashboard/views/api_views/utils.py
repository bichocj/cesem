from rest_framework import serializers

class BasePathSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    # this method allows create route for detail page as /api/activity/1/
    def get_url(self, obj):      
       return "/api/%s/%i/" % (self.get_path() , obj.id)
    
    # this method allows create route for detail page as /api/activity/
    def get_home_path(self):      
       return "/api/%s/" % self.get_path()
    
    # this method allows create route as router.register(r'%s' % ActivityPathSerializer.get_path(), ActivityViewSet)
    @classmethod
    def get_path(cls):
        raise NotImplementedError("'get_path' method should be implemented in '%s' class" % cls.__name__)
