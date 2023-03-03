import plotly.express as px

new_profile = 'фигзнает'
fig = px.scatter(new_profile[:100],
          x='followers',
          y='total_stars',
          color='forks',
          size='contribution')
fig.show()