from itsdangerous import URLSafeTimedSerializer

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(')gw@m$^!&pg%(cg1c@1+5jg9^y#%(sddb@xw6bw-r-nw=_0hbz')
    return serializer.dumps(email, salt='0(lzpu^!5o&*$gj55#e_(+$373qe_q2q&v*fijb8m6sqnlj32x')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(')gw@m$^!&pg%(cg1c@1+5jg9^y#%(sddb@xw6bw-r-nw=_0hbz')
    try:
        email = serializer.loads(
            token,
            salt='0(lzpu^!5o&*$gj55#e_(+$373qe_q2q&v*fijb8m6sqnlj32x',
            max_age=expiration
        )
    except:
        return False
    return email