def model_unicode(instance, fields):
    vals = [getattr(instance, x) for x in fields]

    def force_unicode(s):
        if isinstance(s, str):
            return s.decode('utf-8') 
        return unicode(s)

    return u'{}({})'.format(
        instance.__class__.__name__,
        u', '.join([force_unicode(v) for v in vals])
    )
