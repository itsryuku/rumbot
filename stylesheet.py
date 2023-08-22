class Stylesheets:
    @staticmethod
    def button_style():
      return """
        QPushButton {
            max-width: 70px;
            background-color: #464646;
            color: #FFA116;
            padding: 7px 10px;
            font-family: 'Montserrat', sans-serif;
            font-size: 13px;
        }
        QPushButton:hover {
            background-color: #555555; /* Change the color when hovering */
        }
    """

    def input_style():
      return """
              background-color: #373737;
              min-width: 60px;
              border-radius: 3px;
              padding: 5px;
              color: #FFFFFF;
              font-family: Lato;
              font-size: 14px;
              font-style: italic;
      """
    def label_style():
      return """
          color: white;
          font-weight: bold;
          font-family: 'Lato', sans-serif;
          font-size: 13px;
      """
    def noti_style():
        return """
            text-align: center;
            font-family: Lato;
            font-size: 13px;
            font-style: italic;
      """