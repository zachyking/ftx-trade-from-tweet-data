import tweepy
import re
import trade

bearer = "<twitter_bearer>"

#Listener Class Override
class StreamListener(tweepy.StreamingClient):

	def on_tweet(self, tweet):
		try:
			tweet_content: str = str(tweet).replace("tweet ", "", 1)

			#ignore retweets but print them out
			if tweet_content.startswith('RT'):
				print('retweet', tweet)
				return

			core: float = -100
			headline: float = -100

			for tweet_line in tweet_content.splitlines():
				if not tweet_line.startswith('U.S.'):
					continue
				elif tweet_line.lower().find('core') >= 0:
					tmp_nums = re.findall(r'[\d]*[.][\d]+', tweet_line)
					if len(tmp_nums) > 0:
						core = float(tmp_nums[0])
					else:
						break
				else:
					tmp_nums = re.findall(r'[\d]*[.][\d]+', tweet_line)
					if len(tmp_nums) > 0:
						headline = float(tmp_nums[0])
					else:
						break
			if headline == -100 or core == -100:
				print('failed getting correct values from tweet:', tweet)
			else:
				trade.strategy(core=core, headline=headline)

				print('headline', headline)
				print('core', core)
			

		except Exception as e:
			print('failed on_tweet', tweet)
			print(e)

	def on_error(self, status):
		print(status)


stream = StreamListener(bearer)

stream.add_rules(add=[
 		tweepy.StreamRule("from:Tree_of_Alpha", "From Tree Of Alpha", 1580320836266991617),
	]
)
stream.filter()

