from tkinter import Tk, Canvas, PhotoImage, Button
import os
import sys

window = Tk()
window.geometry("1300x1000")
c = Canvas(window, width = 1300, height = 1000)
c.pack()

class square(object):
    def __init__(self, canvas_x, canvas_y, piece, piece_color, x, y, name):
        self.canvas_x = canvas_x
        self.canvas_y = canvas_y
        self.piece = piece
        self.piece_color = piece_color
        self.x = x
        self.y = y
        self.name = name
    def display_moves(self, *args):
        #debugging feature:
        #print(self.get_name(), self.get_piece(), self.get_color())
        global is_any_square_clicked
        global currently_clicked_square
        global current_player
        global currently_displayed_moves
        global white_short_flag
        global white_long_flag
        global black_short_flag
        global black_long_flag
        global current_list_of_images
        global en_passant_mark
        global fifty_move_counter

        temp_currently_clicked_square = currently_clicked_square
        if currently_clicked_square != None:
            temp_current_piece = currently_clicked_square.piece

        if is_any_square_clicked == True:
            if self in currently_displayed_moves:
                #this checks if en passant occures
                if ((self.piece == None) and (temp_current_piece == "white_pawn" or temp_current_piece == "black_pawn")
                        and (self.x != temp_currently_clicked_square.x)):
                    self.place_piece(currently_clicked_square.get_piece(), currently_clicked_square.get_color())
                    currently_clicked_square.place_piece(None, None)
                    if temp_current_piece == "white_pawn":
                        LIST_OF_COLUMNS[self.x][self.y - 1].place_piece(None, None)
                    else:
                        LIST_OF_COLUMNS[self.x][self.y + 1].place_piece(None, None)
                    current_list_of_images = piece_layout_update()
                    currently_clicked_square.hide_moves()
                    destroy_proper_accept_draw_button()
                    if current_player == "white":
                        current_player = "black"
                    else:
                        current_player = "white"
                    en_passant_mark = None
                    fifty_move_counter = 0
                    square.mate_or_stalemate()
                    return(0)
                #this checks if promotion occures
                if ((self.y == 0 or self.y == 7) 
                        and (temp_current_piece == "white_pawn"
                        or temp_current_piece == "black_pawn")):
                    self.promotion_choice(currently_clicked_square.piece_color)
                    return(0)
                #this checks if en passant should be possible on the next move
                if ((currently_clicked_square.y == 1 and self.y == 3 and temp_current_piece == "white_pawn")
                        or (currently_clicked_square.y == 6 and self.y == 4 and temp_current_piece == "black_pawn")):
                    en_passant_mark = self
                else:
                    en_passant_mark = None
                if self == h1:
                    white_short_flag = 0
                elif self == a1:
                    white_long_flag = 0
                elif self == h8:
                    black_short_flag = 0
                elif self == a8:
                    black_long_flag = 0
                prior_piece_count = square.piece_counter()
                self.place_piece(currently_clicked_square.get_piece(), currently_clicked_square.get_color())
                currently_clicked_square.place_piece(None, None)
                current_list_of_images = piece_layout_update()
                currently_clicked_square.hide_moves()
                destroy_proper_accept_draw_button()
                if current_player == "white":
                    current_player = "black"
                else:
                    current_player = "white"
                if temp_current_piece == "white_king":
                    white_short_flag = 0
                    white_long_flag = 0
                elif temp_current_piece == "black_king":
                    black_short_flag = 0
                    black_long_flag = 0
                elif temp_currently_clicked_square == h1:
                    white_short_flag = 0
                elif temp_currently_clicked_square == a1:
                    white_long_flag = 0
                elif temp_currently_clicked_square == h8:
                    black_short_flag = 0
                elif temp_currently_clicked_square == a8:
                    black_long_flag = 0
                square.mate_or_stalemate()
                after_piece_count = square.piece_counter()
                if (after_piece_count != prior_piece_count 
                    or temp_current_piece == "white_pawn" 
                    or temp_current_piece == "black_pawn"):
                    fifty_move_counter = 0
                else:
                    square.fifty_move_rule()
                #list_of_moves_update(self, currently_clicked_square, check_status)
                return (0)
            
            elif self == g1 and "white_short_castle" in currently_displayed_moves:
                e1.place_piece(None, None)
                h1.place_piece(None, None)
                g1.place_piece("white_king", "white")
                f1.place_piece("white_rook", "white")
                current_list_of_images = piece_layout_update()
                currently_clicked_square.hide_moves()
                destroy_proper_accept_draw_button()
                current_player = "black"
                white_short_flag = 0
                white_long_flag = 0
                en_passant_mark = None
                square.mate_or_stalemate()
                square.fifty_move_rule()
                return (0)
            
            elif self == c1 and "white_long_castle" in currently_displayed_moves:
                e1.place_piece(None, None)
                a1.place_piece(None, None)
                c1.place_piece("white_king", "white")
                d1.place_piece("white_rook", "white")
                current_list_of_images = piece_layout_update()
                currently_clicked_square.hide_moves()
                destroy_proper_accept_draw_button()
                current_player = "black"
                white_short_flag = 0
                white_long_flag = 0
                en_passant_mark = None
                square.mate_or_stalemate()
                square.fifty_move_rule()
                return (0)

            elif self == g8 and "black_short_castle" in currently_displayed_moves:
                e8.place_piece(None, None)
                h8.place_piece(None, None)
                g8.place_piece("black_king", "black")
                f8.place_piece("black_rook", "black")
                current_list_of_images = piece_layout_update()
                currently_clicked_square.hide_moves()
                destroy_proper_accept_draw_button()
                current_player = "white"
                black_short_flag = 0
                black_long_flag = 0
                en_passant_mark = None
                square.mate_or_stalemate()
                square.fifty_move_rule()
                return (0)
            
            elif self == c8 and "black_long_castle" in currently_displayed_moves:
                e8.place_piece(None, None)
                a8.place_piece(None, None)
                c8.place_piece("black_king", "black")
                d8.place_piece("black_rook", "black")
                current_list_of_images = piece_layout_update()
                currently_clicked_square.hide_moves()
                destroy_proper_accept_draw_button()
                current_player = "white"
                black_short_flag = 0
                black_long_flag = 0
                en_passant_mark = None
                square.mate_or_stalemate()
                square.fifty_move_rule()
                return (0)
            
            else:
                currently_clicked_square.hide_moves()
            
        if self.piece_color == current_player:
            if temp_currently_clicked_square == self:
                self.hide_moves()
                return(0)
            moves = self.determine_legal_moves()
            if moves == []:
                return(0)
            else:
                currently_displayed_moves = moves
                is_any_square_clicked = True
                currently_clicked_square = self
                for move in moves:
                    if type(move) == str:
                        match move:
                            case "white_short_castle":
                                c.create_image(g1.get_coords(), image = krompka, anchor = "nw", tag = "krompka")
                                c.tag_raise(f"rect_g1")
                            case "white_long_castle":
                                c.create_image(c1.get_coords(), image = krompka, anchor = "nw", tag = "krompka")
                                c.tag_raise(f"rect_c1")
                            case "black_short_castle":
                                c.create_image(g8.get_coords(), image = krompka, anchor = "nw", tag = "krompka")
                                c.tag_raise(f"rect_g8")
                            case "black_long_castle":
                                c.create_image(c8.get_coords(), image = krompka, anchor = "nw", tag = "krompka")
                                c.tag_raise(f"rect_c8")
                    else:
                        if move.get_piece() == None:
                            c.create_image(move.get_coords(), image = krompka, anchor = "nw", tag = "krompka")
                            c.tag_raise(f"rect_{move.get_name()}")
                        else:
                            c.create_image(move.get_coords(), image = ramka, anchor = "nw", tag = "ramka")
                            c.tag_raise(f"rect_{move.get_name()}")
        return(0)
    
    def hide_moves(self):
        global is_any_square_clicked
        global currently_displayed_moves
        global currently_clicked_square
        c.delete("krompka")
        c.delete("ramka")
        square.hide_promotion_choice()
        currently_clicked_square = None
        is_any_square_clicked = False
        currently_displayed_moves = []

    def place_piece(self, new_piece, new_piece_color):
        self.piece = new_piece
        self.piece_color = new_piece_color
        return(0)
    
    def get_name(self):
        return(self.name)
    def get_coords(self):
        return(self.canvas_x, self.canvas_y)
    def get_color(self):
        return(self.piece_color)
    def get_piece(self):
        return(self.piece)

    def determine_legal_moves(self):
        match self.piece:
            case None:
                pass
            case "white_rook" | "black_rook":
                legal_moves = []
                temp_x = self.x
                temp_y = self.y
                while temp_x < 7:
                    temp_x += 1
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y])
                        if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                            break
                    else:
                        break
                temp_x = self.x
                while temp_x > 0:
                    temp_x -= 1
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y])
                        if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                            break
                    else:
                        break
                temp_x = self.x
                while temp_y < 7:
                    temp_y += 1
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y])
                        if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                            break
                    else:
                        break
                temp_y = self.y
                while temp_y > 0:
                    temp_y -= 1
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y])
                        if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                            break
                    else:
                        break
                
            case "white_knight" | "black_knight":
                legal_moves = []
                temp_x = self.x
                temp_y = self.y
                if temp_x < 7 and temp_y < 6:
                    new_x = temp_x + 1
                    new_y = temp_y + 2
                    if LIST_OF_COLUMNS[new_x][new_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x < 7 and temp_y > 1:
                    new_x = temp_x + 1
                    new_y = temp_y - 2
                    if LIST_OF_COLUMNS[new_x][new_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x < 6 and temp_y < 7:
                    new_x = temp_x + 2
                    new_y = temp_y + 1
                    if LIST_OF_COLUMNS[new_x][new_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x > 1 and temp_y < 7:
                    new_x = temp_x - 2
                    new_y = temp_y + 1
                    if LIST_OF_COLUMNS[new_x][new_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x > 0 and temp_y < 6:
                    new_x = temp_x - 1
                    new_y = temp_y + 2
                    if LIST_OF_COLUMNS[new_x][new_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x > 0 and temp_y > 1:
                    new_x = temp_x - 1
                    new_y = temp_y - 2
                    if LIST_OF_COLUMNS[new_x][new_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x < 6 and temp_y > 0:
                    new_x = temp_x + 2
                    new_y = temp_y - 1
                    if LIST_OF_COLUMNS[new_x][new_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x > 1 and temp_y > 0:
                    new_x = temp_x - 2
                    new_y = temp_y - 1
                    if LIST_OF_COLUMNS[new_x][new_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[new_x][new_y])

            case "white_bishop" | "black_bishop":
                legal_moves = []
                temp_x, temp_y = self.x, self.y
                while temp_x < 7 and temp_y < 7:
                    temp_x += 1
                    temp_y += 1
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y])
                        if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                            break
                    else:
                        break
                temp_x, temp_y = self.x, self.y
                while temp_x < 7 and temp_y > 0:
                    temp_x += 1
                    temp_y -=1
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y])
                        if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                            break
                    else:
                        break
                temp_x, temp_y = self.x, self.y
                while temp_x > 0 and temp_y > 0:
                    temp_x -= 1
                    temp_y -=1
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y])
                        if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                            break
                    else:
                        break
                temp_x, temp_y = self.x, self.y
                while temp_x > 0 and temp_y < 7:
                    temp_x -= 1
                    temp_y +=1
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y])
                        if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                            break
                    else:
                        break

            case "white_queen" | "black_queen":
                self.place_piece(f"{self.get_color()}_rook", self.get_color())
                rook_like_moves = self.determine_legal_moves()
                self.place_piece(f"{self.get_color()}_bishop", self.get_color())
                bishop_like_moves = self.determine_legal_moves()
                legal_moves = bishop_like_moves + rook_like_moves
                self.place_piece(f"{self.get_color()}_queen", self.get_color())

            case "white_king" | "black_king":
                legal_moves = []

                if self.x < 7:
                    if LIST_OF_COLUMNS[self.x + 1][self.y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[self.x + 1][self.y])

                if self.x < 7 and self.y > 0:
                    if LIST_OF_COLUMNS[self.x + 1][self.y - 1].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[self.x + 1][self.y - 1])

                if self.x < 7 and self.y < 7:
                    if LIST_OF_COLUMNS[self.x + 1][self.y + 1].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[self.x + 1][self.y + 1])

                if self.x > 0:
                    if LIST_OF_COLUMNS[self.x - 1][self.y].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[self.x - 1][self.y])

                if self.x > 0 and self.y > 0:
                    if LIST_OF_COLUMNS[self.x - 1][self.y - 1].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[self.x - 1][self.y - 1])

                if self.x > 0 and self.y < 7:
                    if LIST_OF_COLUMNS[self.x - 1][self.y + 1].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[self.x - 1][self.y + 1])

                if self.y > 0:
                    if LIST_OF_COLUMNS[self.x][self.y - 1].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[self.x][self.y - 1])

                if self.y < 7:
                    if LIST_OF_COLUMNS[self.x][self.y + 1].piece_color != self.piece_color:
                        legal_moves.append(LIST_OF_COLUMNS[self.x][self.y + 1])
                
                global white_short_flag
                if (white_short_flag == 1 and self.piece == "white_king" and
                        f1.piece == None and g1.piece == None):
                    legal_moves.append("white_short_castle")

                global white_long_flag
                if (white_long_flag == 1 and self.piece == "white_king" and
                        b1.piece == None and c1.piece == None and 
                        d1.piece == None):
                    legal_moves.append("white_long_castle")

                global black_short_flag
                if (black_short_flag == 1 and self.piece == "black_king" and
                        f8.piece == None and g8.piece == None):
                    legal_moves.append("black_short_castle")

                global black_long_flag
                if (black_long_flag == 1 and self.piece == "black_king" and
                        b8.piece == None and c8.piece == None and 
                        d8.piece == None):
                    legal_moves.append("black_long_castle")

            case "white_pawn":
                legal_moves = []
                temp_x = self.x
                temp_y = self.y
                for count in range(2):
                    if LIST_OF_COLUMNS[temp_x][temp_y + 1].piece_color == None:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y + 1])
                    else:
                        break
                    if temp_y == 1 and LIST_OF_COLUMNS[temp_x][temp_y + 2].piece_color == None:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y + 2])
                if temp_x < 7 and LIST_OF_COLUMNS[temp_x + 1][temp_y + 1].piece_color == "black":
                        legal_moves.append(LIST_OF_COLUMNS[temp_x + 1][temp_y + 1])
                if temp_x > 0 and LIST_OF_COLUMNS[temp_x - 1][temp_y + 1].piece_color == "black":
                        legal_moves.append(LIST_OF_COLUMNS[temp_x - 1][temp_y + 1])
                #en passant
                try:
                    if en_passant_mark.x > 0:
                        if en_passant_mark.x - 1 == self.x and self.y == 4:
                            legal_moves.append(LIST_OF_COLUMNS[en_passant_mark.x][en_passant_mark.y + 1])
                    if en_passant_mark.x < 7:
                        if en_passant_mark.x + 1 == self.x and self.y == 4:
                            legal_moves.append(LIST_OF_COLUMNS[en_passant_mark.x][en_passant_mark.y + 1])
                except AttributeError:
                    pass

                    
            case "black_pawn":
                legal_moves = []
                temp_x = self.x
                temp_y = self.y
                for count in range(2):
                    if LIST_OF_COLUMNS[temp_x][temp_y - 1].piece_color == None:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y - 1])
                    else:
                        break
                    if temp_y == 6 and LIST_OF_COLUMNS[temp_x][temp_y - 2].piece_color == None:
                        legal_moves.append(LIST_OF_COLUMNS[temp_x][temp_y - 2])
                if temp_x < 7 and LIST_OF_COLUMNS[temp_x + 1][temp_y - 1].piece_color == "white":
                        legal_moves.append(LIST_OF_COLUMNS[temp_x + 1][temp_y - 1])
                if temp_x > 0 and LIST_OF_COLUMNS[temp_x - 1][temp_y - 1].piece_color == "white":
                        legal_moves.append(LIST_OF_COLUMNS[temp_x - 1][temp_y - 1])
                #en passant
                try:
                    if en_passant_mark.x > 0:
                        if en_passant_mark.x - 1 == self.x and self.y == 3:
                            legal_moves.append(LIST_OF_COLUMNS[en_passant_mark.x][en_passant_mark.y - 1])
                    if en_passant_mark.x < 7:
                        if en_passant_mark.x + 1 == self.x and self.y == 3:
                            legal_moves.append(LIST_OF_COLUMNS[en_passant_mark.x][en_passant_mark.y - 1])
                except AttributeError:
                    pass

        actual_legal_moves = self.illegal_moves_excluder(legal_moves)
        return(actual_legal_moves)
            
    def determine_threatened_squares(self):
        threatened_squares = []
        match self.piece:
            case None:
                pass
            case "white_rook" | "black_rook":
                temp_x = self.x
                temp_y = self.y
                while temp_x < 7:
                    temp_x += 1
                    threatened_squares.append(LIST_OF_COLUMNS[temp_x][temp_y])
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                        break
                temp_x = self.x
                while temp_x > 0:
                    temp_x -= 1
                    threatened_squares.append(LIST_OF_COLUMNS[temp_x][temp_y])
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                        break
                temp_x = self.x
                while temp_y < 7:
                    temp_y += 1
                    threatened_squares.append(LIST_OF_COLUMNS[temp_x][temp_y])
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                        break
                temp_y = self.y
                while temp_y > 0:
                    temp_y -= 1
                    threatened_squares.append(LIST_OF_COLUMNS[temp_x][temp_y])
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                        break
            case "white_knight" | "black_knight":
                temp_x = self.x
                temp_y = self.y
                if temp_x < 7 and temp_y < 6:
                    new_x = temp_x + 1
                    new_y = temp_y + 2
                    threatened_squares.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x < 7 and temp_y > 1:
                    new_x = temp_x + 1
                    new_y = temp_y - 2
                    threatened_squares.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x < 6 and temp_y < 7:
                    new_x = temp_x + 2
                    new_y = temp_y + 1
                    threatened_squares.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x > 1 and temp_y < 7:
                    new_x = temp_x - 2
                    new_y = temp_y + 1
                    threatened_squares.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x > 0 and temp_y < 6:
                    new_x = temp_x - 1
                    new_y = temp_y + 2
                    threatened_squares.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x > 0 and temp_y > 1:
                    new_x = temp_x - 1
                    new_y = temp_y - 2
                    threatened_squares.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x < 6 and temp_y > 0:
                    new_x = temp_x + 2
                    new_y = temp_y - 1
                    threatened_squares.append(LIST_OF_COLUMNS[new_x][new_y])
                if temp_x > 1 and temp_y > 0:
                    new_x = temp_x - 2
                    new_y = temp_y - 1
                    threatened_squares.append(LIST_OF_COLUMNS[new_x][new_y])
            case "white_bishop" | "black_bishop":
                temp_x, temp_y = self.x, self.y
                while temp_x < 7 and temp_y < 7:
                    temp_x += 1
                    temp_y += 1
                    threatened_squares.append(LIST_OF_COLUMNS[temp_x][temp_y])
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                        break
                temp_x, temp_y = self.x, self.y
                while temp_x < 7 and temp_y > 0:
                    temp_x += 1
                    temp_y -=1
                    threatened_squares.append(LIST_OF_COLUMNS[temp_x][temp_y])
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                        break
                temp_x, temp_y = self.x, self.y
                while temp_x > 0 and temp_y > 0:
                    temp_x -= 1
                    temp_y -=1
                    threatened_squares.append(LIST_OF_COLUMNS[temp_x][temp_y])
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                        break
                temp_x, temp_y = self.x, self.y
                while temp_x > 0 and temp_y < 7:
                    temp_x -= 1
                    temp_y +=1
                    threatened_squares.append(LIST_OF_COLUMNS[temp_x][temp_y])
                    if LIST_OF_COLUMNS[temp_x][temp_y].piece_color != None:
                        break
            case "white_queen" | "black_queen":
                self.place_piece(f"{self.get_color()}_rook", self.get_color())
                rook_like_threats = self.determine_threatened_squares()
                self.place_piece(f"{self.get_color()}_bishop", self.get_color())
                bishop_like_threats = self.determine_threatened_squares()
                threatened_squares.extend(bishop_like_threats)
                threatened_squares.extend(rook_like_threats)
                self.place_piece(f"{self.get_color()}_queen", self.get_color())
            case "white_king" | "black_king":
                if self.x < 7:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x + 1][self.y])
                if self.x > 0:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x - 1][self.y])
                if self.y < 7:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x][self.y + 1])
                if self.y > 0:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x][self.y - 1])
                if self.x < 7 and self.y < 7:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x + 1][self.y + 1])
                if self.x < 7 and self.y > 0:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x + 1][self.y - 1])
                if self.x > 0 and self.y < 7:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x - 1][self.y + 1])
                if self.x > 0 and self.y > 0:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x - 1][self.y - 1])
            case "white_pawn":
                if self.x < 7:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x + 1][self.y + 1])
                if self.x > 0:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x - 1][self.y + 1])
            case "black_pawn":
                if self.x < 7:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x + 1][self.y - 1])
                if self.x > 0:
                    threatened_squares.append(LIST_OF_COLUMNS[self.x - 1][self.y - 1])
        return(threatened_squares)
    
    def illegal_moves_excluder(self, legal_moves):
        actual_legal_moves = []
        for move in legal_moves:
            if type(move) == str:
                match move:
                    case "white_short_castle":
                        if (e1 not in square.determine_all_threatened_squares()
                                and f1 not in square.determine_all_threatened_squares()
                                and g1 not in square.determine_all_threatened_squares()):
                            actual_legal_moves.append(move)
                    case "white_long_castle":
                        if (e1 not in square.determine_all_threatened_squares()
                                and d1 not in square.determine_all_threatened_squares()
                                and c1 not in square.determine_all_threatened_squares()):
                            actual_legal_moves.append(move)
                    case "black_short_castle":
                        if (e8 not in square.determine_all_threatened_squares()
                                and f8 not in square.determine_all_threatened_squares()
                                and g8 not in square.determine_all_threatened_squares()):
                            actual_legal_moves.append(move)
                    case "black_long_castle":
                        if (e8 not in square.determine_all_threatened_squares()
                                and d8 not in square.determine_all_threatened_squares()
                                and c8 not in square.determine_all_threatened_squares()):
                            actual_legal_moves.append(move)  
            else:
                #to do: add an if clause for en passant
                original_piece = move.piece
                original_piece_color = move.piece_color
                move.piece = self.piece
                move.piece_color = self.piece_color
                self.piece = None
                self.piece_color = None
                if not square.check_if_check(square.determine_kings_position(), square.determine_all_threatened_squares()):
                    actual_legal_moves.append(move)
                self.piece = move.piece
                self.piece_color = move.piece_color
                move.piece = original_piece
                move.piece_color = original_piece_color
        return(actual_legal_moves)
    
    def promotion_choice(self, pawns_color):
        global currently_clicked_square
        global is_any_square_clicked
        temp_currently_clicked_square = currently_clicked_square
        currently_clicked_square.hide_moves()
        currently_clicked_square = temp_currently_clicked_square
        is_any_square_clicked = True

        promotion_background = c.create_rectangle(self.canvas_x, self.canvas_y, self.canvas_x + rect_height, self.canvas_y + rect_width, 
                                                  fill = "white", tag = "promotion_background")
        match pawns_color:
            case "white":
                small_queen_image = c.create_image(self.canvas_x, self.canvas_y, image = small_white_queen, anchor = "nw", tag = "small_queen_image")
                small_rook_image = c.create_image(self.canvas_x + 50, self.canvas_y, image = small_white_rook, anchor = "nw", tag = "small_rook_image")
                small_knight_image = c.create_image(self.canvas_x, self.canvas_y + 50, image = small_white_knight, anchor = "nw", tag = "small_knight_image")
                small_bishop_image = c.create_image(self.canvas_x + 50, self.canvas_y + 50, image = small_white_bishop, anchor = "nw", tag = "small_bishop_image")
                c.tag_bind("small_queen_image", "<Button-1>", self.white_queen_promotion)
                c.tag_bind("small_rook_image", "<Button-1>", self.white_rook_promotion)
                c.tag_bind("small_knight_image", "<Button-1>", self.white_knight_promotion)
                c.tag_bind("small_bishop_image", "<Button-1>", self.white_bishop_promotion)
            case "black":
                small_queen_image = c.create_image(self.canvas_x, self.canvas_y, image = small_black_queen, anchor = "nw", tag = "small_queen_image")
                small_rook_image = c.create_image(self.canvas_x + 50, self.canvas_y, image = small_black_rook, anchor = "nw", tag = "small_rook_image")
                small_knight_image = c.create_image(self.canvas_x, self.canvas_y + 50, image = small_black_knight, anchor = "nw", tag = "small_knight_image")
                small_bishop_image = c.create_image(self.canvas_x + 50, self.canvas_y + 50, image = small_black_bishop, anchor = "nw", tag = "small_bishop_image")
                c.tag_bind("small_queen_image", "<Button-1>", self.black_queen_promotion)
                c.tag_bind("small_rook_image", "<Button-1>", self.black_rook_promotion)
                c.tag_bind("small_knight_image", "<Button-1>", self.black_knight_promotion)
                c.tag_bind("small_bishop_image", "<Button-1>", self.black_bishop_promotion)
        return(0)
        
    def promotion(self, chosen_piece, pawns_color):
        global white_short_flag
        global white_long_flag
        global black_short_flag
        global black_long_flag
        global current_list_of_images
        global current_player
        global en_passant_mark
        global fifty_move_counter

        if self == h1:
            white_short_flag = 0
        elif self == a1:
            white_long_flag = 0
        elif self == h8:
            black_short_flag = 0
        elif self == a8:
            black_long_flag = 0
        self.place_piece(chosen_piece, pawns_color)
        currently_clicked_square.place_piece(None, None)
        current_list_of_images = piece_layout_update()
        currently_clicked_square.hide_moves()
        destroy_proper_accept_draw_button()
        if current_player == "white":
            current_player = "black"
        else:
            current_player = "white"
        en_passant_mark = None
        fifty_move_counter = 0
        square.mate_or_stalemate()
        return(0)
    
    def white_queen_promotion(self, *args):
        self.promotion("white_queen", "white")
    def white_rook_promotion(self, *args):
        self.promotion("white_rook", "white")
    def white_knight_promotion(self, *args):
        self.promotion("white_knight", "white")
    def white_bishop_promotion(self, *args):
        self.promotion("white_bishop", "white")
    def black_queen_promotion(self, *args):
        self.promotion("black_queen", "black")
    def black_rook_promotion(self, *args):
        self.promotion("black_rook", "black")
    def black_knight_promotion(self, *args):
        self.promotion("black_knight", "black")
    def black_bishop_promotion(self, *args):
        self.promotion("black_bishop", "black")

    @staticmethod
    def hide_promotion_choice():
        c.delete("promotion_background")
        c.delete("small_queen_image")
        c.delete("small_rook_image")
        c.delete("small_knight_image")
        c.delete("small_bishop_image")
        return(0)

    @staticmethod
    def determine_all_threatened_squares():
        global LIST_OF_SQUARES
        global current_player
        all_threatened_squares = set()
        for instance_of_a_square in LIST_OF_SQUARES:
            if (instance_of_a_square.piece_color != current_player 
                    and instance_of_a_square.piece_color != None):
                all_threatened_squares.update(instance_of_a_square.determine_threatened_squares())
        return(all_threatened_squares)
    
    @staticmethod
    def determine_kings_position():
        global current_player
        if current_player == "white":
            for instance_of_a_square in LIST_OF_SQUARES:
                if instance_of_a_square.piece == "white_king":
                    kings_position = instance_of_a_square
                    break
        else:
            for instance_of_a_square in LIST_OF_SQUARES:
                if instance_of_a_square.piece == "black_king":
                    kings_position = instance_of_a_square
                    break
        return(kings_position)
    
    @staticmethod
    def check_if_check(kings_position, threatened_squares):
        if kings_position in threatened_squares:
            check_status = True
        else:
            check_status = False
        return(check_status)
    
    @staticmethod
    def mate_or_stalemate():
        for instance_of_a_square in LIST_OF_SQUARES:
            global current_player
            if instance_of_a_square.piece_color == current_player:
                if not instance_of_a_square.determine_legal_moves():
                    continue
                else:
                    square.repetition_list_appender()
                    square.insufficient_material_rule()
                    return(False)
        if square.check_if_check(square.determine_kings_position(), square.determine_all_threatened_squares()):
            if current_player == "white":
                win_text("Black")
            else:
                
                win_text("White")
        else:
            draw_text("stalemate")
        
    @staticmethod
    def repetition_list_appender():
        current_board_state = dict(zip([x.get_name() for x in LIST_OF_SQUARES], [x.piece for x in LIST_OF_SQUARES]))
        global board_state_list
        global repeated_board_state_list
        global current_player
        if current_board_state in board_state_list:
            if current_board_state in repeated_board_state_list:
                draw_text("repetition")
            else:
                repeated_board_state_list.append(current_board_state)
        else:
            board_state_list.append(current_board_state)

    @staticmethod
    def piece_counter():
        piece_count = 0
        for instance_of_a_square in LIST_OF_SQUARES:
            if instance_of_a_square.piece != None:
                piece_count += 1
        return(piece_count)
    
    @staticmethod
    def fifty_move_rule():
        global fifty_move_counter
        global current_player
        fifty_move_counter += 1
        if fifty_move_counter == 100:
            draw_text("fifty move rule")

    @staticmethod
    def insufficient_material_rule():
        first_condition = sorted(["white_king", "black_king"])
        second_condition_a = sorted(["white_king", "black_king", "white_bishop"])
        second_condition_b = sorted(["white_king", "black_king", "black_bishop"])
        third_condition_a = sorted(["white_king", "black_king", "white_knight"])
        third_condition_b = sorted(["white_king", "black_king", "black_knight"])
        fourth_condition = sorted(["white_king", "black_king", "white_bishop", "black_bishop"])

        list_of_material = []
        for instance_of_a_square in LIST_OF_SQUARES:
            if instance_of_a_square.piece != None:
                list_of_material.append(instance_of_a_square.piece)
        list_of_material.sort()

        #this checks if bishops are on a different colored squares
        revised_fourth_condition = False
        if list_of_material == fourth_condition:
            for instance_of_a_square in LIST_OF_SQUARES:
                match instance_of_a_square.piece:
                    case "white_bishop":
                        white_bishop_x = instance_of_a_square.x
                        white_bishop_y = instance_of_a_square.y
                        white_bishop_sum = white_bishop_x + white_bishop_y
                    case "black_bishop":
                        black_bishop_x = instance_of_a_square.x
                        black_bishop_y = instance_of_a_square.y
                        black_bishop_sum = black_bishop_x + black_bishop_y
            if (white_bishop_sum % 2) != (black_bishop_sum % 2):
                revised_fourth_condition = True

        if ((list_of_material == first_condition) or (list_of_material == second_condition_a)
                or (list_of_material == second_condition_b) or (list_of_material == third_condition_a)
                or (list_of_material == third_condition_b) or revised_fourth_condition):
            draw_text("insufficient material")

#Making sure pictures open correctly no matter where the file is and preparing a transparent bitmap, necessary for invisible rectangles
scriptpath = os.path.abspath(__file__)
scriptdir = os.path.dirname(scriptpath) + "/Obrazy/"
bitmap_path = os.path.join(scriptdir, "transparent_bitmap.xbm")

rect_width = 100
rect_height = 100
rect_color_1 = "#6D523B"
rect_color_2 = "#90826D"        

#a function updating the piece layout
def piece_layout_update():
    list_of_images = []
    for instance_of_a_square in LIST_OF_SQUARES:
        piece = instance_of_a_square.get_piece()
        if piece == None:
            continue
        canvas_x, canvas_y = instance_of_a_square.get_coords()
        image_of_a_piece = PhotoImage(file = os.path.join(scriptdir, f"{piece}.png"))
        list_of_images.append(image_of_a_piece)
        square_name = instance_of_a_square.get_name()
        c.create_image(canvas_x, canvas_y, image = image_of_a_piece, anchor = "nw")
        c.tag_raise(f"rect_{square_name}")
    return(list_of_images)


small_white_queen = PhotoImage(file = os.path.join(scriptdir, "small_white_queen.png"))
small_white_rook = PhotoImage(file = os.path.join(scriptdir, "small_white_rook.png"))
small_white_knight = PhotoImage(file = os.path.join(scriptdir, "small_white_knight.png"))
small_white_bishop = PhotoImage(file = os.path.join(scriptdir, "small_white_bishop.png"))
small_black_queen = PhotoImage(file = os.path.join(scriptdir, "small_black_queen.png"))
small_black_rook = PhotoImage(file = os.path.join(scriptdir, "small_black_rook.png"))
small_black_knight = PhotoImage(file = os.path.join(scriptdir, "small_black_knight.png"))
small_black_bishop = PhotoImage(file = os.path.join(scriptdir, "small_black_bishop.png"))

def both_players_legal_moves_printer():
    for instance_of_a_square in LIST_OF_SQUARES:
        if (instance_of_a_square.determine_legal_moves()) != None:
            names_of_legal_moves = []
            for move in instance_of_a_square.determine_legal_moves():
                names_of_legal_moves.append(move.get_name())
            print(f"{instance_of_a_square.get_name()}:{instance_of_a_square.get_piece()}:{names_of_legal_moves}")
            
krompka = PhotoImage(file = os.path.join(scriptdir, "krompka.png"))
ramka = PhotoImage(file = os.path.join(scriptdir, "frame.png"))

#def show_threats():
    #threatened_squares = square.determine_all_threatened_squares()
    #for threatened_square in threatened_squares:
        #c.create_image(threatened_square.get_coords(), image = krompka, anchor = "nw", tag = "krompka")

def play_again():
    #python = sys.executable
    #os.execl(python, python, * sys.argv)
    play_again_button.destroy()
    play()

def create_play_again_button():
    global play_again_button
    play_again_button = Button(c, width = '20', height = '2', background = "Brown", font = ("Times new roman", 20), text = "Play again?", command = play_again)
    play_again_button.place(x = 350, y = 901)

def win_text(color):
    white_resign_button.destroy()
    black_resign_button.destroy()
    if color == "White":
        opposite_color = "Black"
    elif color == "Black":
        opposite_color = "White"
    text_background = c.create_rectangle(300, 400, 700, 600, fill = opposite_color)
    white_win_text = c.create_text(500, 500, fill = color, text = f"{color} wins!", font = ("Times new roman", 50, "bold"), anchor = "center")
    destroy_all_buttons()
    create_play_again_button()

def draw_text(reason):
    global current_player
    text_background = c.create_rectangle(100, 400, 900, 600, fill = "White")
    white_win_text = c.create_text(500, 500, fill = "Black", text = f"Draw by {reason}", font = ("Times new roman", 45, "bold"), anchor = "center")
    current_player = None
    destroy_all_buttons()
    create_play_again_button()

def white_resign():
    win_text("Black")

def black_resign():
    win_text("White")

def create_white_draw_offer_button():
    global white_draw_offer_button
    white_draw_offer_button = Button(c, width = '10', height = '2', background = "white", foreground = "black",
                                    font = ("Times new roman", 20), text = "Offer draw", command = create_black_accept_draw_button)
    white_draw_offer_button.place(x = 1120, y = 800)

def create_black_draw_offer_button():
    global black_draw_offer_button
    black_draw_offer_button = Button(c, width = '10', height = '2', background = "black", foreground = "white",
                                    font = ("Times new roman", 20), text = "Offer draw", command = create_white_accept_draw_button)
    black_draw_offer_button.place(x = 1120, y = 100)

def create_white_accept_draw_button():
    black_draw_offer_button.destroy()
    global white_accept_draw_button
    white_accept_draw_button = Button(c, width = '10', height = '2', background = "white", foreground = "black",
                                    font = ("Times new roman", 20), text = "Accept draw?", command = accept_draw_offer)
    white_accept_draw_button.place(x = 1120, y = 800)
    global white_accept_draw_flag
    white_accept_draw_flag = 1

def create_black_accept_draw_button():
    white_draw_offer_button.destroy()
    global black_accept_draw_button
    black_accept_draw_button = Button(c, width = '10', height = '2', background = "black", foreground = "white",
                                    font = ("Times new roman", 20), text = "Accept draw?", command = accept_draw_offer)
    black_accept_draw_button.place(x = 1120, y = 100)
    global black_accept_draw_flag
    black_accept_draw_flag = 1

def accept_draw_offer():
    draw_text("agreement")

def destroy_all_buttons():
    global white_resign_button, black_resign_button
    white_resign_button.destroy()
    black_resign_button.destroy()
    try:
        white_draw_offer_button.destroy()
    except NameError:
        pass
    try:
        black_draw_offer_button.destroy()
    except NameError:
        pass
    try:
        white_accept_draw_button.destroy()
    except NameError:
        pass
    try:
        black_accept_draw_button.destroy()
    except NameError:
        pass



def destroy_proper_accept_draw_button():
    if current_player == "white":
        global white_accept_draw_flag
        if white_accept_draw_flag:
            white_accept_draw_button.destroy()
            create_black_draw_offer_button()
            white_accept_draw_flag = 0
    else:
        global black_accept_draw_flag
        if black_accept_draw_flag:
            black_accept_draw_button.destroy()
            create_white_draw_offer_button()
            black_accept_draw_flag = 0


          
def play():       
    #initialiasing flags used to determine if castling should be a legal move
    global white_short_flag, white_long_flag, black_short_flag, black_long_flag
    white_short_flag = 1
    white_long_flag = 1
    black_short_flag = 1
    black_long_flag = 1

    global current_player, is_any_square_clicked, currently_clicked_square, currently_displayed_moves, en_passant_mark, fifty_move_counter, list_of_moves, white_accept_draw_flag, black_accept_draw_flag
    current_player = "white"
    is_any_square_clicked = False
    currently_clicked_square = None
    currently_displayed_moves = []
    en_passant_mark = None
    fifty_move_counter = 0
    list_of_moves = []
    white_accept_draw_flag = 0
    black_accept_draw_flag = 0

    #def list_of_moves_update(starting_square, finish_square)
    #    for instance_of_a_square in LIST_OF_SQUARES:
    #        if instance_of_a_square == starting_square:
    #            pass
    #        elif instance_of_a_square.piece == starting_square.piece:

    global a1, a2, a3, a4, a5, a6, a7, a8
    global b1, b2, b3, b4, b5, b6, b7, b8
    global c1, c2, c3, c4, c5, c6, c7, c8
    global d1, d2, d3, d4, d5, d6, d7, d8
    global e1, e2, e3, e4, e5, e6, e7, e8
    global f1, f2, f3, f4, f5, f6, f7, f8
    global g1, g2, g3, g4, g5, g6, g7, g8
    global h1, h2, h3, h4, h5, h6, h7, h8

    a1=square(100, 800, "white_rook","white",0,0,"a1")
    a2=square(100, 700, "white_pawn","white",0,1,"a2")
    a3=square(100, 600, None,None,0,2,"a3")
    a4=square(100, 500, None,None,0,3,"a4")
    a5=square(100, 400, None,None,0,4,"a5")
    a6=square(100, 300, None,None,0,5,"a6")
    a7=square(100, 200, "black_pawn","black",0,6,"a7")
    a8=square(100, 100, "black_rook","black",0,7,"a8")
    b1=square(200, 800, "white_knight","white",1,0,"b1")
    b2=square(200, 700, "white_pawn","white",1,1,"b2")
    b3=square(200, 600, None,None,1,2,"b3")
    b4=square(200, 500, None,None,1,3,"b4")
    b5=square(200, 400, None,None,1,4,"b5")
    b6=square(200, 300, None,None,1,5,"b6")
    b7=square(200, 200, "black_pawn","black",1,6,"b7")
    b8=square(200, 100, "black_knight","black",1,7,"b8")
    c1=square(300, 800, "white_bishop","white",2,0,"c1")
    c2=square(300, 700, "white_pawn","white",2,1,"c2")
    c3=square(300, 600, None,None,2,2,"c3")
    c4=square(300, 500, None,None,2,3,"c4")
    c5=square(300, 400, None,None,2,4,"c5")
    c6=square(300, 300, None,None,2,5,"c6")
    c7=square(300, 200, "black_pawn","black",2,6,"c7")
    c8=square(300, 100, "black_bishop","black",2,7,"c8")
    d1=square(400, 800, "white_queen","white",3,0,"d1")
    d2=square(400, 700, "white_pawn","white",3,1,"d2")
    d3=square(400, 600, None,None,3,2,"d3")
    d4=square(400, 500, None,None,3,3,"d4")
    d5=square(400, 400, None,None,3,4,"d5")
    d6=square(400, 300, None,None,3,5,"d6")
    d7=square(400, 200, "black_pawn","black",3,6,"d7")
    d8=square(400, 100, "black_queen","black",3,7,"d8")
    e1=square(500, 800, "white_king","white",4,0,"e1")
    e2=square(500, 700, "white_pawn","white",4,1,"e2")
    e3=square(500, 600, None,None,4,2,"e3")
    e4=square(500, 500, None,None,4,3,"e4")
    e5=square(500, 400, None,None,4,4,"e5")
    e6=square(500, 300, None,None,4,5,"e6")
    e7=square(500, 200, "black_pawn","black",4,6,"e7")
    e8=square(500, 100, "black_king","black",4,7,"e8")
    f1=square(600, 800, "white_bishop","white",5,0,"f1")
    f2=square(600, 700, "white_pawn","white",5,1,"f2")
    f3=square(600, 600, None,None,5,2,"f3")
    f4=square(600, 500, None,None,5,3,"f4")
    f5=square(600, 400, None,None,5,4,"f5")
    f6=square(600, 300, None,None,5,5,"f6")
    f7=square(600, 200, "black_pawn","black",5,6,"f7")
    f8=square(600, 100, "black_bishop","black",5,7,"f8")
    g1=square(700, 800, "white_knight","white",6,0,"g1")
    g2=square(700, 700, "white_pawn","white",6,1,"g2")
    g3=square(700, 600, None,None,6,2,"g3")
    g4=square(700, 500, None,None,6,3,"g4")
    g5=square(700, 400, None,None,6,4,"g5")
    g6=square(700, 300, None,None,6,5,"g6")
    g7=square(700, 200, "black_pawn","black",6,6,"g7")
    g8=square(700, 100, "black_knight","black",6,7,"g8")
    h1=square(800, 800, "white_rook","white",7,0,"h1")
    h2=square(800, 700, "white_pawn","white",7,1,"h2")
    h3=square(800, 600, None,None,7,2,"h3")
    h4=square(800, 500, None,None,7,3,"h4")
    h5=square(800, 400, None,None,7,4,"h5")
    h6=square(800, 300, None,None,7,5,"h6")
    h7=square(800, 200, "black_pawn","black",7,6,"h7")
    h8=square(800, 100, "black_rook","black",7,7,"h8")

    COLUMN_A = (a1, a2, a3, a4, a5, a6, a7, a8)
    COLUMN_B = (b1, b2, b3, b4, b5, b6, b7, b8)
    COLUMN_C = (c1, c2, c3, c4, c5, c6, c7, c8)
    COLUMN_D = (d1, d2, d3, d4, d5, d6, d7, d8)
    COLUMN_E = (e1, e2, e3, e4, e5, e6, e7, e8)
    COLUMN_F = (f1, f2, f3, f4, f5, f6, f7, f8)
    COLUMN_G = (g1, g2, g3, g4, g5, g6, g7, g8)
    COLUMN_H = (h1, h2, h3, h4, h5, h6, h7, h8)

    global LIST_OF_SQUARES, LIST_OF_COLUMNS
    LIST_OF_SQUARES = COLUMN_A + COLUMN_B + COLUMN_C + COLUMN_D + COLUMN_E + COLUMN_F + COLUMN_G + COLUMN_H
    LIST_OF_COLUMNS = (COLUMN_A, COLUMN_B, COLUMN_C, COLUMN_D, COLUMN_E, COLUMN_F, COLUMN_G, COLUMN_H)

    global board_state_list, repeated_board_state_list
    board_state_list = [dict(zip([x.get_name() for x in LIST_OF_SQUARES], [x.piece for x in LIST_OF_SQUARES]))]
    repeated_board_state_list = []



    rect_a1 = c.create_rectangle(100, 800, 100 + rect_width, 800 + rect_height, fill = rect_color_1)
    rect_a2 = c.create_rectangle(100, 700, 100 + rect_width, 700 + rect_height, fill = rect_color_2)
    rect_a3 = c.create_rectangle(100, 600, 100 + rect_width, 600 + rect_height, fill = rect_color_1)
    rect_a4 = c.create_rectangle(100, 500, 100 + rect_width, 500 + rect_height, fill = rect_color_2)
    rect_a5 = c.create_rectangle(100, 400, 100 + rect_width, 400 + rect_height, fill = rect_color_1)
    rect_a6 = c.create_rectangle(100, 300, 100 + rect_width, 300 + rect_height, fill = rect_color_2)
    rect_a7 = c.create_rectangle(100, 200, 100 + rect_width, 200 + rect_height, fill = rect_color_1)
    rect_a8 = c.create_rectangle(100, 100, 100 + rect_width, 100 + rect_height, fill = rect_color_2)
    rect_b1 = c.create_rectangle(200, 800, 200 + rect_width, 800 + rect_height, fill = rect_color_2)
    rect_b2 = c.create_rectangle(200, 700, 200 + rect_width, 700 + rect_height, fill = rect_color_1)
    rect_b3 = c.create_rectangle(200, 600, 200 + rect_width, 600 + rect_height, fill = rect_color_2)
    rect_b4 = c.create_rectangle(200, 500, 200 + rect_width, 500 + rect_height, fill = rect_color_1)
    rect_b5 = c.create_rectangle(200, 400, 200 + rect_width, 400 + rect_height, fill = rect_color_2)
    rect_b6 = c.create_rectangle(200, 300, 200 + rect_width, 300 + rect_height, fill = rect_color_1)
    rect_b7 = c.create_rectangle(200, 200, 200 + rect_width, 200 + rect_height, fill = rect_color_2)
    rect_b8 = c.create_rectangle(200, 100, 200 + rect_width, 100 + rect_height, fill = rect_color_1)
    rect_c1 = c.create_rectangle(300, 800, 300 + rect_width, 800 + rect_height, fill = rect_color_1)
    rect_c2 = c.create_rectangle(300, 700, 300 + rect_width, 700 + rect_height, fill = rect_color_2)
    rect_c3 = c.create_rectangle(300, 600, 300 + rect_width, 600 + rect_height, fill = rect_color_1)
    rect_c4 = c.create_rectangle(300, 500, 300 + rect_width, 500 + rect_height, fill = rect_color_2)
    rect_c5 = c.create_rectangle(300, 400, 300 + rect_width, 400 + rect_height, fill = rect_color_1)
    rect_c6 = c.create_rectangle(300, 300, 300 + rect_width, 300 + rect_height, fill = rect_color_2)
    rect_c7 = c.create_rectangle(300, 200, 300 + rect_width, 200 + rect_height, fill = rect_color_1)
    rect_c8 = c.create_rectangle(300, 100, 300 + rect_width, 100 + rect_height, fill = rect_color_2)
    rect_d1 = c.create_rectangle(400, 800, 400 + rect_width, 800 + rect_height, fill = rect_color_2)
    rect_d2 = c.create_rectangle(400, 700, 400 + rect_width, 700 + rect_height, fill = rect_color_1)
    rect_d3 = c.create_rectangle(400, 600, 400 + rect_width, 600 + rect_height, fill = rect_color_2)
    rect_d4 = c.create_rectangle(400, 500, 400 + rect_width, 500 + rect_height, fill = rect_color_1)
    rect_d5 = c.create_rectangle(400, 400, 400 + rect_width, 400 + rect_height, fill = rect_color_2)
    rect_d6 = c.create_rectangle(400, 300, 400 + rect_width, 300 + rect_height, fill = rect_color_1)
    rect_d7 = c.create_rectangle(400, 200, 400 + rect_width, 200 + rect_height, fill = rect_color_2)
    rect_d8 = c.create_rectangle(400, 100, 400 + rect_width, 100 + rect_height, fill = rect_color_1)
    rect_e1 = c.create_rectangle(500, 800, 500 + rect_width, 800 + rect_height, fill = rect_color_1)
    rect_e2 = c.create_rectangle(500, 700, 500 + rect_width, 700 + rect_height, fill = rect_color_2)
    rect_e3 = c.create_rectangle(500, 600, 500 + rect_width, 600 + rect_height, fill = rect_color_1)
    rect_e4 = c.create_rectangle(500, 500, 500 + rect_width, 500 + rect_height, fill = rect_color_2)
    rect_e5 = c.create_rectangle(500, 400, 500 + rect_width, 400 + rect_height, fill = rect_color_1)
    rect_e6 = c.create_rectangle(500, 300, 500 + rect_width, 300 + rect_height, fill = rect_color_2)
    rect_e7 = c.create_rectangle(500, 200, 500 + rect_width, 200 + rect_height, fill = rect_color_1)
    rect_e8 = c.create_rectangle(500, 100, 500 + rect_width, 100 + rect_height, fill = rect_color_2)
    rect_f1 = c.create_rectangle(600, 800, 600 + rect_width, 800 + rect_height, fill = rect_color_2)
    rect_f2 = c.create_rectangle(600, 700, 600 + rect_width, 700 + rect_height, fill = rect_color_1)
    rect_f3 = c.create_rectangle(600, 600, 600 + rect_width, 600 + rect_height, fill = rect_color_2)
    rect_f4 = c.create_rectangle(600, 500, 600 + rect_width, 500 + rect_height, fill = rect_color_1)
    rect_f5 = c.create_rectangle(600, 400, 600 + rect_width, 400 + rect_height, fill = rect_color_2)
    rect_f6 = c.create_rectangle(600, 300, 600 + rect_width, 300 + rect_height, fill = rect_color_1)
    rect_f7 = c.create_rectangle(600, 200, 600 + rect_width, 200 + rect_height, fill = rect_color_2)
    rect_f8 = c.create_rectangle(600, 100, 600 + rect_width, 100 + rect_height, fill = rect_color_1)
    rect_g1 = c.create_rectangle(700, 800, 700 + rect_width, 800 + rect_height, fill = rect_color_1)
    rect_g2 = c.create_rectangle(700, 700, 700 + rect_width, 700 + rect_height, fill = rect_color_2)
    rect_g3 = c.create_rectangle(700, 600, 700 + rect_width, 600 + rect_height, fill = rect_color_1)
    rect_g4 = c.create_rectangle(700, 500, 700 + rect_width, 500 + rect_height, fill = rect_color_2)
    rect_g5 = c.create_rectangle(700, 400, 700 + rect_width, 400 + rect_height, fill = rect_color_1)
    rect_g6 = c.create_rectangle(700, 300, 700 + rect_width, 300 + rect_height, fill = rect_color_2)
    rect_g7 = c.create_rectangle(700, 200, 700 + rect_width, 200 + rect_height, fill = rect_color_1)
    rect_g8 = c.create_rectangle(700, 100, 700 + rect_width, 100 + rect_height, fill = rect_color_2)
    rect_h1 = c.create_rectangle(800, 800, 800 + rect_width, 800 + rect_height, fill = rect_color_2)
    rect_h2 = c.create_rectangle(800, 700, 800 + rect_width, 700 + rect_height, fill = rect_color_1)
    rect_h3 = c.create_rectangle(800, 600, 800 + rect_width, 600 + rect_height, fill = rect_color_2)
    rect_h4 = c.create_rectangle(800, 500, 800 + rect_width, 500 + rect_height, fill = rect_color_1)
    rect_h5 = c.create_rectangle(800, 400, 800 + rect_width, 400 + rect_height, fill = rect_color_2)
    rect_h6 = c.create_rectangle(800, 300, 800 + rect_width, 300 + rect_height, fill = rect_color_1)
    rect_h7 = c.create_rectangle(800, 200, 800 + rect_width, 200 + rect_height, fill = rect_color_2)
    rect_h8 = c.create_rectangle(800, 100, 800 + rect_width, 100 + rect_height, fill = rect_color_1)




    #to jakbym zapomniał jak robić obrazki xd
    #c.create_image(100, 100, image = black_bishop, anchor = "nw", tags = "black_bishop")

    #As the pieces are placed on and cover squares, and linking a piece to a square it's on would be a daunting task, 
    #I'm creating an invisible rectangle on top of each square
    transparent_rect_a1 = c.create_rectangle(100, 800, 100 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a1")
    transparent_rect_a1 = c.create_rectangle(100, 800, 100 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a1")
    transparent_rect_a1 = c.create_rectangle(100, 800, 100 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a1")
    transparent_rect_a1 = c.create_rectangle(100, 800, 100 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a1")
    transparent_rect_a1 = c.create_rectangle(100, 800, 100 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a1")
    transparent_rect_a1 = c.create_rectangle(100, 800, 100 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a1")
    transparent_rect_a1 = c.create_rectangle(100, 800, 100 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a1")
    transparent_rect_a1 = c.create_rectangle(100, 800, 100 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a1")
    transparent_rect_a1 = c.create_rectangle(100, 800, 100 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a1")
    transparent_rect_a2 = c.create_rectangle(100, 700, 100 + rect_width, 700 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a2")
    transparent_rect_a3 = c.create_rectangle(100, 600, 100 + rect_width, 600 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a3")
    transparent_rect_a4 = c.create_rectangle(100, 500, 100 + rect_width, 500 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a4")
    transparent_rect_a5 = c.create_rectangle(100, 400, 100 + rect_width, 400 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a5")
    transparent_rect_a6 = c.create_rectangle(100, 300, 100 + rect_width, 300 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a6")
    transparent_rect_a7 = c.create_rectangle(100, 200, 100 + rect_width, 200 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a7")
    transparent_rect_a8 = c.create_rectangle(100, 100, 100 + rect_width, 100 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_a8")
    transparent_rect_b1 = c.create_rectangle(200, 800, 200 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_b1")
    transparent_rect_b2 = c.create_rectangle(200, 700, 200 + rect_width, 700 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_b2")
    transparent_rect_b3 = c.create_rectangle(200, 600, 200 + rect_width, 600 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_b3")
    transparent_rect_b4 = c.create_rectangle(200, 500, 200 + rect_width, 500 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_b4")
    transparent_rect_b5 = c.create_rectangle(200, 400, 200 + rect_width, 400 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_b5")
    transparent_rect_b6 = c.create_rectangle(200, 300, 200 + rect_width, 300 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_b6")
    transparent_rect_b7 = c.create_rectangle(200, 200, 200 + rect_width, 200 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_b7")
    transparent_rect_b8 = c.create_rectangle(200, 100, 200 + rect_width, 100 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_b8")
    transparent_rect_c1 = c.create_rectangle(300, 800, 300 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_c1")
    transparent_rect_c2 = c.create_rectangle(300, 700, 300 + rect_width, 700 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_c2")
    transparent_rect_c3 = c.create_rectangle(300, 600, 300 + rect_width, 600 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_c3")
    transparent_rect_c4 = c.create_rectangle(300, 500, 300 + rect_width, 500 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_c4")
    transparent_rect_c5 = c.create_rectangle(300, 400, 300 + rect_width, 400 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_c5")
    transparent_rect_c6 = c.create_rectangle(300, 300, 300 + rect_width, 300 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_c6")
    transparent_rect_c7 = c.create_rectangle(300, 200, 300 + rect_width, 200 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_c7")
    transparent_rect_c8 = c.create_rectangle(300, 100, 300 + rect_width, 100 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_c8")
    transparent_rect_d1 = c.create_rectangle(400, 800, 400 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_d1")
    transparent_rect_d2 = c.create_rectangle(400, 700, 400 + rect_width, 700 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_d2")
    transparent_rect_d3 = c.create_rectangle(400, 600, 400 + rect_width, 600 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_d3")
    transparent_rect_d4 = c.create_rectangle(400, 500, 400 + rect_width, 500 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_d4")
    transparent_rect_d5 = c.create_rectangle(400, 400, 400 + rect_width, 400 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_d5")
    transparent_rect_d6 = c.create_rectangle(400, 300, 400 + rect_width, 300 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_d6")
    transparent_rect_d7 = c.create_rectangle(400, 200, 400 + rect_width, 200 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_d7")
    transparent_rect_d8 = c.create_rectangle(400, 100, 400 + rect_width, 100 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_d8")
    transparent_rect_e1 = c.create_rectangle(500, 800, 500 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_e1")
    transparent_rect_e2 = c.create_rectangle(500, 700, 500 + rect_width, 700 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_e2")
    transparent_rect_e3 = c.create_rectangle(500, 600, 500 + rect_width, 600 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_e3")
    transparent_rect_e4 = c.create_rectangle(500, 500, 500 + rect_width, 500 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_e4")
    transparent_rect_e5 = c.create_rectangle(500, 400, 500 + rect_width, 400 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_e5")
    transparent_rect_e6 = c.create_rectangle(500, 300, 500 + rect_width, 300 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_e6")
    transparent_rect_e7 = c.create_rectangle(500, 200, 500 + rect_width, 200 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_e7")
    transparent_rect_e8 = c.create_rectangle(500, 100, 500 + rect_width, 100 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_e8")
    transparent_rect_f1 = c.create_rectangle(600, 800, 600 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_f1")
    transparent_rect_f2 = c.create_rectangle(600, 700, 600 + rect_width, 700 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_f2")
    transparent_rect_f3 = c.create_rectangle(600, 600, 600 + rect_width, 600 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_f3")
    transparent_rect_f4 = c.create_rectangle(600, 500, 600 + rect_width, 500 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_f4")
    transparent_rect_f5 = c.create_rectangle(600, 400, 600 + rect_width, 400 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_f5")
    transparent_rect_f6 = c.create_rectangle(600, 300, 600 + rect_width, 300 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_f6")
    transparent_rect_f7 = c.create_rectangle(600, 200, 600 + rect_width, 200 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_f7")
    transparent_rect_f8 = c.create_rectangle(600, 100, 600 + rect_width, 100 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_f8")
    transparent_rect_g1 = c.create_rectangle(700, 800, 700 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_g1")
    transparent_rect_g2 = c.create_rectangle(700, 700, 700 + rect_width, 700 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_g2")
    transparent_rect_g3 = c.create_rectangle(700, 600, 700 + rect_width, 600 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_g3")
    transparent_rect_g4 = c.create_rectangle(700, 500, 700 + rect_width, 500 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_g4")
    transparent_rect_g5 = c.create_rectangle(700, 400, 700 + rect_width, 400 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_g5")
    transparent_rect_g6 = c.create_rectangle(700, 300, 700 + rect_width, 300 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_g6")
    transparent_rect_g7 = c.create_rectangle(700, 200, 700 + rect_width, 200 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_g7")
    transparent_rect_g8 = c.create_rectangle(700, 100, 700 + rect_width, 100 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_g8")
    transparent_rect_h1 = c.create_rectangle(800, 800, 800 + rect_width, 800 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_h1")
    transparent_rect_h2 = c.create_rectangle(800, 700, 800 + rect_width, 700 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_h2")
    transparent_rect_h3 = c.create_rectangle(800, 600, 800 + rect_width, 600 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_h3")
    transparent_rect_h4 = c.create_rectangle(800, 500, 800 + rect_width, 500 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_h4")
    transparent_rect_h5 = c.create_rectangle(800, 400, 800 + rect_width, 400 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_h5")
    transparent_rect_h6 = c.create_rectangle(800, 300, 800 + rect_width, 300 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_h6")
    transparent_rect_h7 = c.create_rectangle(800, 200, 800 + rect_width, 200 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_h7")
    transparent_rect_h8 = c.create_rectangle(800, 100, 800 + rect_width, 100 + rect_height, fill = "gray", stipple = f"@{bitmap_path}", width = 0, tags = "rect_h8")


    #Making each square (by actually making an invisible rectangle on top of it) clickable
    for instance_of_a_square in LIST_OF_SQUARES:
        current_square = instance_of_a_square.get_name()
        c.tag_bind(f"rect_{current_square}", "<Button-1>", instance_of_a_square.display_moves)

    create_white_draw_offer_button()
    create_black_draw_offer_button()

    global white_resign_button, black_resign_button
    white_resign_button = Button(c, width = '10', height = '2', background = "white", foreground = "black",
                            font = ("Times new roman", 20), text = "Resign", command = white_resign)
    white_resign_button.place(x = 920, y = 800)
    black_resign_button = Button(c, width = '10', height = '2', background = "black", foreground = "white",
                            font = ("Times new roman", 20), text = "Resign", command = black_resign)
    black_resign_button.place(x = 920, y = 100)

    global current_list_of_images
    current_list_of_images = piece_layout_update()

play()
window.mainloop()