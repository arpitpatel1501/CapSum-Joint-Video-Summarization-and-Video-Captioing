import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
//720//https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_1280_10MG.mp4
//680//https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_640_3MG.mp4
const useStyles = makeStyles({
  root: {
    maxWidth: 500,
  },
});

export default function VidCard(props) {
  const classes = useStyles();
  return (
    <Card elevation={10} className={classes.root}>
      <CardActionArea onClick={props.onLog}>
        <CardMedia
          component="img"
          //height="150"
          height={props.height}
          width={props.width}
          image={props.image}
        />
        <CardContent >
          <Typography variant="h5" component="h2" >
            {props.title}
          </Typography>
        </CardContent>
      </CardActionArea>
      
    </Card>
  );
}