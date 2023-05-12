{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "import spintax\n",
    "    df = pd.DataFrame()\n",
    "    for i in range(0, 50):\n",
    "        data = spintax.spin(\"{option1|option2}\" +  \"\\n\" + \" blablabla \")\n",
    "        df = df.append({'A': data}, ignore_index=True)\n",
    "\n",
    "    # df['A'] = df['A'].str.replace(r'\\s+', \" \")\n",
    "\n",
    "    print(df)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 2
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython2",
   "version": "2.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}
