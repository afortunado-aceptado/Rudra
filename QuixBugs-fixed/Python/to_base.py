import string
def to_base(num, b):
    result = ''
    alphabet = string.digits + string.ascii_uppercase
    while num > 0:
        i = num % b
        num = num // b
        result = alphabet[i] + result # corrected line
    return result
'''
The\ issue\ with\ the\ original\ code\ was\ that\ it\ appended\ the\ new\ digit\ or\ letter\ to\ the\ end\ of\ the\ result\ string,\ instead\ of\ adding\ it\ to\ the\ beginning.\ This\ caused\ the\ output\ to\ be\ in\ reverse\ order.\ By\ changing\ result\ =\ result\ +\ alphabet[i]\ to\ result\ =\ alphabet[i]\ +\ result,\ we\ ensure\ that\ each\ new\ character\ is\ added\ to\ the\ front\ of\ the\ string,\ thereby\ producing\ the\ correct\ order\ for\ the\ base\ conversion.\ This\ adjustment\ allows\ the\ function\ to\ accurately\ convert\ the\ base-10\ integer\ to\ the\ specified\ target\ base\ and\ pass\ all\ the\ test\ cases.

'''